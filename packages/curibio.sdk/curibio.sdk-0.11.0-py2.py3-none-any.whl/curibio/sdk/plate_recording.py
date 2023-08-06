# -*- coding: utf-8 -*-
"""Docstring."""
import datetime
import logging
import os
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union
import uuid
from uuid import UUID
import zipfile

from mantarray_file_manager import MAIN_FIRMWARE_VERSION_UUID
from mantarray_file_manager import MANTARRAY_SERIAL_NUMBER_UUID
from mantarray_file_manager import METADATA_UUID_DESCRIPTIONS
from mantarray_file_manager import PLATE_BARCODE_UUID
from mantarray_file_manager import PlateRecording as FileManagerPlateRecording
from mantarray_file_manager import SOFTWARE_BUILD_NUMBER_UUID
from mantarray_file_manager import SOFTWARE_RELEASE_VERSION_UUID
from mantarray_file_manager import UTC_BEGINNING_RECORDING_UUID
from mantarray_file_manager import WellFile
from mantarray_waveform_analysis import AMPLITUDE_UUID
from mantarray_waveform_analysis import CENTIMILLISECONDS_PER_SECOND
from mantarray_waveform_analysis import CONTRACTION_VELOCITY_UUID
from mantarray_waveform_analysis import Pipeline
from mantarray_waveform_analysis import PipelineTemplate
from mantarray_waveform_analysis import RELAXATION_VELOCITY_UUID
from mantarray_waveform_analysis import TooFewPeaksDetectedError
from mantarray_waveform_analysis import TWITCH_FREQUENCY_UUID
from mantarray_waveform_analysis import TWITCH_PERIOD_UUID
from mantarray_waveform_analysis import TwoPeaksInARowError
from mantarray_waveform_analysis import TwoValleysInARowError
from mantarray_waveform_analysis import WIDTH_UUID
from mantarray_waveform_analysis import WIDTH_VALUE_UUID
from mantarray_waveform_analysis.exceptions import PeakDetectionError
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from nptyping import NDArray
import numpy as np
from scipy import interpolate
from stdlib_utils import configure_logging
import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.utility import xl_col_to_name

from .constants import AGGREGATE_METRICS_SHEET_NAME
from .constants import ALL_FORMATS
from .constants import CALCULATED_METRIC_DISPLAY_NAMES
from .constants import CHART_FIXED_WIDTH
from .constants import CHART_FIXED_WIDTH_CELLS
from .constants import CHART_HEIGHT
from .constants import CHART_HEIGHT_CELLS
from .constants import CHART_WINDOW_NUM_SECONDS
from .constants import CONTINUOUS_WAVEFORM_SHEET_NAME
from .constants import DEFAULT_CELL_WIDTH
from .constants import FORCE_FREQUENCY_RELATIONSHIP_SHEET
from .constants import FULL_CHART_SHEET_NAME
from .constants import INTERPOLATED_DATA_PERIOD_CMS
from .constants import INTERPOLATED_DATA_PERIOD_SECONDS
from .constants import METADATA_EXCEL_SHEET_NAME
from .constants import METADATA_INSTRUMENT_ROW_START
from .constants import METADATA_OUTPUT_FILE_ROW_START
from .constants import METADATA_RECORDING_ROW_START
from .constants import MICROSECONDS_PER_CENTIMILLISECOND
from .constants import NUMBER_OF_PER_TWITCH_METRICS
from .constants import PACKAGE_VERSION
from .constants import PEAK_VALLEY_COLUMN_START
from .constants import PER_TWITCH_METRICS_SHEET_NAME
from .constants import SECONDS_PER_CELL
from .constants import SNAPSHOT_CHART_SHEET_NAME
from .constants import TSP_TO_DEFAULT_FILTER_UUID
from .constants import TWENTY_FOUR_WELL_PLATE
from .constants import TWITCH_FREQUENCIES_CHART_SHEET_NAME
from .excel_well_file import ExcelWellFile

logger = logging.getLogger(__name__)
configure_logging(logging_format="notebook")


def _write_per_twitch_metric_labels(
    curr_sheet: xlsxwriter.worksheet.Worksheet,
    curr_row: int,
) -> int:
    for (
        _,
        iter_metric_name,
    ) in CALCULATED_METRIC_DISPLAY_NAMES.items():
        if isinstance(iter_metric_name, tuple):
            _, iter_metric_name = iter_metric_name
        curr_sheet.write(curr_row, 0, iter_metric_name)
        curr_row += 1
    return curr_row


def _write_per_twitch_metric_values(
    curr_sheet: xlsxwriter.worksheet.Worksheet,
    curr_row: int,
    per_twitch_dict: Dict[
        int,
        Dict[
            UUID,
            Union[
                Dict[int, Dict[UUID, Union[Tuple[int, int], int]]],
                Union[float, int],
            ],
        ],
    ],
    number_twitches: int,
) -> int:
    for iter_twitch_index in range(number_twitches):
        curr_sheet.write(
            curr_row, iter_twitch_index + 1, f"Twitch {iter_twitch_index + 1}"
        )

    curr_row += 1

    twitch_timepoints = list(per_twitch_dict)

    for iter_twitch_index in range(number_twitches):
        curr_sheet.write(
            curr_row,
            iter_twitch_index + 1,
            twitch_timepoints[iter_twitch_index] / CENTIMILLISECONDS_PER_SECOND,
        )

    curr_row += 1
    for (
        iter_metric_uuid,
        iter_metric_name,
    ) in CALCULATED_METRIC_DISPLAY_NAMES.items():
        if isinstance(iter_metric_name, tuple):
            iter_width_percent, iter_metric_name = iter_metric_name
        for iter_twitch_index in range(number_twitches):
            timepoint = twitch_timepoints[iter_twitch_index]
            value_to_write = per_twitch_dict[timepoint][iter_metric_uuid]
            if iter_metric_uuid == WIDTH_UUID:
                if not isinstance(value_to_write, dict):
                    raise NotImplementedError(
                        f"The width value under key {WIDTH_VALUE_UUID} must be a dictionary."
                    )
                value_to_write = (
                    value_to_write[iter_width_percent][WIDTH_VALUE_UUID]
                    / CENTIMILLISECONDS_PER_SECOND
                )
            if iter_metric_uuid == TWITCH_PERIOD_UUID:
                value_to_write /= CENTIMILLISECONDS_PER_SECOND
            if iter_metric_uuid in (
                CONTRACTION_VELOCITY_UUID,
                RELAXATION_VELOCITY_UUID,
            ):
                value_to_write *= CENTIMILLISECONDS_PER_SECOND
            curr_sheet.write(curr_row, iter_twitch_index + 1, value_to_write)

        curr_row += 1

    curr_row -= 9  # revert back to initial row (number of metrics + 1)
    return curr_row


def _write_xlsx_device_metadata(
    curr_sheet: xlsxwriter.worksheet.Worksheet, first_well_file: WellFile
) -> None:
    curr_row = METADATA_INSTRUMENT_ROW_START
    curr_sheet.write(curr_row, 0, "Device Information:")
    curr_row += 1
    curr_sheet.write(curr_row, 1, "H5 File Layout Version")
    curr_sheet.write(
        curr_row, 2, first_well_file.get_h5_attribute("File Format Version")
    )
    curr_row += 1
    for iter_row, (iter_metadata_uuid, iter_value) in enumerate(
        (
            (
                MANTARRAY_SERIAL_NUMBER_UUID,
                first_well_file.get_mantarray_serial_number(),
            ),
            (
                SOFTWARE_RELEASE_VERSION_UUID,
                first_well_file.get_h5_attribute(str(SOFTWARE_RELEASE_VERSION_UUID)),
            ),
            (
                SOFTWARE_BUILD_NUMBER_UUID,
                first_well_file.get_h5_attribute(str(SOFTWARE_BUILD_NUMBER_UUID)),
            ),
            (
                MAIN_FIRMWARE_VERSION_UUID,
                first_well_file.get_h5_attribute(str(MAIN_FIRMWARE_VERSION_UUID)),
            ),
        )
    ):
        row_in_sheet = curr_row + iter_row
        curr_sheet.write(
            row_in_sheet,
            1,
            METADATA_UUID_DESCRIPTIONS[iter_metadata_uuid],
        )
        curr_sheet.write(
            row_in_sheet,
            2,
            iter_value,
        )


def _write_xlsx_output_format_metadata(
    curr_sheet: xlsxwriter.worksheet.Worksheet,
) -> None:
    curr_row = METADATA_OUTPUT_FILE_ROW_START
    curr_sheet.write(curr_row, 0, "Output Format:")
    curr_row += 1
    curr_sheet.write(curr_row, 1, "SDK Version")
    curr_sheet.write(curr_row, 2, PACKAGE_VERSION)
    curr_row += 1
    curr_sheet.write(curr_row, 1, "File Creation Timestamp")
    curr_sheet.write(curr_row, 2, datetime.datetime.utcnow().replace(microsecond=0))


def _write_xlsx_recording_metadata(
    curr_sheet: xlsxwriter.worksheet.Worksheet, first_well_file: WellFile
) -> None:
    curr_sheet.write(METADATA_RECORDING_ROW_START, 0, "Recording Information:")
    for iter_row, (iter_metadata_uuid, iter_value) in enumerate(
        (
            (PLATE_BARCODE_UUID, first_well_file.get_plate_barcode()),
            (UTC_BEGINNING_RECORDING_UUID, first_well_file.get_begin_recording()),
        )
    ):
        row_in_sheet = METADATA_RECORDING_ROW_START + 1 + iter_row
        curr_sheet.write(
            row_in_sheet,
            1,
            METADATA_UUID_DESCRIPTIONS[iter_metadata_uuid],
        )
        if isinstance(iter_value, datetime.datetime):
            # Excel doesn't support timezones in datetimes
            iter_value = iter_value.replace(tzinfo=None)
        curr_sheet.write(
            row_in_sheet,
            2,
            iter_value,
        )


def _write_xlsx_metadata(
    workbook: xlsxwriter.workbook.Workbook, first_well_file: WellFile
) -> None:
    logger.info("Writing H5 file metadata")
    metadata_sheet = workbook.add_worksheet(METADATA_EXCEL_SHEET_NAME)
    curr_sheet = metadata_sheet
    _write_xlsx_recording_metadata(curr_sheet, first_well_file)
    if not isinstance(first_well_file, ExcelWellFile):
        _write_xlsx_device_metadata(curr_sheet, first_well_file)
    _write_xlsx_output_format_metadata(curr_sheet)
    # Adjust the column widths to be able to see the data
    for iter_column_idx, iter_column_width in ((0, 25), (1, 40), (2, 25)):
        curr_sheet.set_column(iter_column_idx, iter_column_idx, iter_column_width)


class PlateRecording(FileManagerPlateRecording):
    """Manages aspects of analyzing a plate recording session."""

    def __init__(
        self,
        *args: Any,
        pipeline_template: Optional[PipelineTemplate] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super().__init__(*args, **kwargs)
        self._is_optical_recording = isinstance(self._files[0], ExcelWellFile)
        self._workbook: xlsxwriter.workbook.Workbook
        self._workbook_formats: Dict[str, Format] = dict()
        if pipeline_template is None:
            first_well_index = self.get_well_indices()[0]
            # this file is used to get general information applicable across the recording
            first_well_file = self.get_well_by_index(first_well_index)
            tissue_sampling_period = (
                first_well_file.get_tissue_sampling_period_microseconds()
                / MICROSECONDS_PER_CENTIMILLISECOND
            )
            noise_filter_uuid = (
                None
                if self._is_optical_recording
                else TSP_TO_DEFAULT_FILTER_UUID[tissue_sampling_period]
            )
            twitches_point_up = False
            if self._is_optical_recording:
                twitches_point_up = first_well_file.get_twitches_point_up()
            pipeline_template = PipelineTemplate(
                tissue_sampling_period=tissue_sampling_period,
                noise_filter_uuid=noise_filter_uuid,
                magnetic_twitches_point_up=twitches_point_up,
            )
        self._pipeline_template = pipeline_template
        self._pipelines: Dict[int, Pipeline]
        self._interpolated_data_period: float

    @classmethod
    def from_directory(cls, dir_to_load_files_from: str) -> "PlateRecording":
        first_item = os.listdir(dir_to_load_files_from)[0]
        if first_item.endswith(".zip"):
            path_to_zip_file = os.path.join(dir_to_load_files_from, first_item)
            with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
                members = [
                    member
                    for member in zip_ref.namelist()
                    if (member.endswith(".h5") or member.endswith(".xlsx"))
                    and "__MACOSX" not in member
                    # Tanner (10/1/20): "__MACOSX" is an artifact of zipping a file on MacOS that is not needed by the SDK. This is likely not a typical use case, but this prevents problems in case a user does zip their files on Mac
                ]
                path_sep = "/"  # Tanner (10/7/20): When zipfile unzips files, it always uses the unix style separator in the names of members
                zip_contains_folder = all(path_sep in member for member in members)
                zip_ref.extractall(dir_to_load_files_from, members=members)
            if zip_contains_folder:
                unzipped_dir_to_load_files_from = os.path.join(
                    dir_to_load_files_from, os.path.dirname(members[0])
                )
                return cls.from_directory(unzipped_dir_to_load_files_from)
            if members[0].endswith(".xlsx"):
                optical_well_files = [
                    ExcelWellFile(os.path.join(dir_to_load_files_from, member))
                    for member in members
                ]
                return cls(optical_well_files)
        if first_item.endswith(".xlsx"):
            optical_well_files = [
                ExcelWellFile(os.path.join(dir_to_load_files_from, item))
                for item in os.listdir(dir_to_load_files_from)
                if item.endswith(".xlsx")
            ]
            return cls(optical_well_files)
        return super().from_directory(dir_to_load_files_from)  # type: ignore # Tanner (10/1/20): Not sure why mypy doesn't see the super class method's return type

    def _init_pipelines(self) -> None:
        try:
            self._pipelines  # pylint:disable=pointless-statement # Eli (9/11/20): this will cause the attribute error to be raised if the pipelines haven't yet been initialized
            return
        except AttributeError:
            pass
        self._pipelines = dict()
        num_wells = len(self.get_well_indices())
        for i, iter_well_idx in enumerate(self.get_well_indices()):
            iter_pipeline = self.get_pipeline_template().create_pipeline()
            well = self.get_well_by_index(iter_well_idx)
            well_name = TWENTY_FOUR_WELL_PLATE.get_well_name_from_well_index(
                iter_well_idx
            )
            msg = f"Loading tissue and reference data... {int(round(i / num_wells, 2) * 100)}% (Well {well_name}, {i + 1} out of {num_wells})"
            logger.info(msg)
            raw_tissue_reading = well.get_raw_tissue_reading()
            if self._is_optical_recording:
                raw_tissue_reading[0] *= CENTIMILLISECONDS_PER_SECOND
            iter_pipeline.load_raw_magnetic_data(
                raw_tissue_reading,
                well.get_raw_reference_reading(),
            )
            self._pipelines[iter_well_idx] = iter_pipeline

    def get_pipeline_template(self) -> PipelineTemplate:
        return self._pipeline_template

    def get_reference_magnetic_data(self, well_idx: int) -> NDArray[(2, Any), int]:
        self._init_pipelines()
        return self._pipelines[well_idx].get_raw_reference_magnetic_data()

    def create_stacked_plot(self) -> Figure:
        """Create a stacked plot of all wells in the recording."""
        # Note Eli (9/11/20): this is hardcoded for a very specific use case at the moment and just visually tested using the newly evolving visual regression tool
        self._init_pipelines()
        factor = 0.25
        plt.figure(figsize=(15 * factor, 35 * 1), dpi=300)
        ax1 = plt.subplot(24, 1, 1)
        ax1.set(ylabel="A1")
        plt.setp(ax1.get_xticklabels(), visible=False)
        count = 0
        for _, iter_pipeline in self._pipelines.items():
            if count == 0:
                pass
            else:
                iter_ax = plt.subplot(24, 1, count + 1, sharex=ax1)
                iter_ax.set(
                    ylabel=TWENTY_FOUR_WELL_PLATE.get_well_name_from_well_index(count)
                )
                if count != 23:
                    plt.setp(iter_ax.get_xticklabels(), visible=False)
                else:
                    iter_ax.set(xlabel="Time (seconds)")
            filtered_data = iter_pipeline.get_noise_filtered_magnetic_data()
            plt.plot(
                filtered_data[0] / CENTIMILLISECONDS_PER_SECOND,
                filtered_data[1],
                linewidth=0.5,
            )
            # plt.plot(filtered_data[0,:int(30*CENTIMILLISECONDS_PER_SECOND/960)]/CENTIMILLISECONDS_PER_SECOND,filtered_data[1,:int(30*CENTIMILLISECONDS_PER_SECOND/960)])
            count += 1
        return plt.gcf()

    def write_xlsx(
        self,
        file_dir: str,
        file_name: Optional[str] = None,
        create_continuous_waveforms: bool = True,
        create_waveform_charts: bool = True,
    ) -> None:
        """Create an XLSX file.

        Args:
            file_dir: the directory in which to create the file.
            file_name: By default an automatic name is generated based on barcode and recording date. Extension will always be xlsx---if user provides something else then it is stripped
            create_continuous_waveforms: typically used in unit testing, if set to True, the continuous-waveforms sheet and continuous-waveform-plots sheet will be created with no content
            create_waveform_charts: typically used in unit testing, if set to True, only the continuous-waveform-plots sheet will be created with no content
        """
        first_well_index = self.get_well_indices()[0]
        # this file is used to get general information applicable across the recording
        first_well_file = self.get_well_by_index(first_well_index)
        logger.info("Loading data from H5 file(s)")
        self._init_pipelines()
        if file_name is None:
            file_name = f"{first_well_file.get_plate_barcode()}__{first_well_file.get_begin_recording().strftime('%Y_%m_%d_%H%M%S')}.xlsx"
        file_path = os.path.join(file_dir, file_name)
        logger.info("Opening .xlsx file")
        self._workbook = Workbook(
            file_path, {"default_date_format": "YYYY-MM-DD hh:mm:ss UTC"}
        )
        for iter_format_name, iter_format in ALL_FORMATS.items():
            self._workbook_formats[iter_format_name] = self._workbook.add_format(
                iter_format
            )
        _write_xlsx_metadata(self._workbook, first_well_file)
        self._write_xlsx_continuous_waveforms(
            skip_content=(not create_continuous_waveforms),
            skip_charts=(not create_waveform_charts),
        )
        self._write_xlsx_aggregate_metrics()
        self._write_xlsx_per_twitch_metrics()
        logger.info("Saving .xlsx file")
        self._workbook.close()  # This is actually when the file gets written to d
        logger.info("Done writing to .xlsx")

    def _write_xlsx_continuous_waveforms(
        self,
        skip_content: bool = False,
        skip_charts: bool = False,
    ) -> None:
        continuous_waveform_sheet = self._workbook.add_worksheet(
            CONTINUOUS_WAVEFORM_SHEET_NAME
        )
        self._workbook.add_worksheet(SNAPSHOT_CHART_SHEET_NAME)
        self._workbook.add_worksheet(FULL_CHART_SHEET_NAME)
        if skip_content:
            return
        logger.info("Creating waveform data sheet")

        curr_sheet = continuous_waveform_sheet

        # create headings
        curr_sheet.write(0, 0, "Time (seconds)")
        for i in range(
            TWENTY_FOUR_WELL_PLATE.row_count * TWENTY_FOUR_WELL_PLATE.column_count
        ):
            curr_sheet.write(
                0, 1 + i, TWENTY_FOUR_WELL_PLATE.get_well_name_from_well_index(i)
            )

        # initialize time values (use longest data)
        max_time_index = 0
        for well_index in self.get_well_indices():
            well_pipeline = self._pipelines[well_index]
            last_time_index = well_pipeline.get_raw_tissue_magnetic_data()[0][-1]
            if last_time_index > max_time_index:
                max_time_index = last_time_index
        self._interpolated_data_period = (
            int(
                self._files[0].get_interpolation_value()
                / MICROSECONDS_PER_CENTIMILLISECOND
            )
            if self._is_optical_recording
            else INTERPOLATED_DATA_PERIOD_CMS
        )
        interpolated_data_indices = np.arange(
            self._interpolated_data_period,  # don't start at time zero, because some wells don't have data at exactly zero (causing interpolation to fail), so just start at the next timepoint
            max_time_index,
            self._interpolated_data_period,
        )

        for i, data_index in enumerate(interpolated_data_indices):
            curr_sheet.write(
                i + 1,
                0,
                data_index
                / CENTIMILLISECONDS_PER_SECOND,  # display in seconds in the Excel sheet
            )

        # add data for valid wells
        well_indices = self.get_well_indices()
        num_wells = len(well_indices)
        for iter_well_idx, well_index in enumerate(well_indices):
            filtered_data = self._pipelines[
                well_index
            ].get_noise_filtered_magnetic_data()
            # interpolate data (at 100 Hz for H5) to max valid interpolated data point
            interpolated_data_function = interpolate.interp1d(
                filtered_data[0], filtered_data[1]
            )
            well_name = TWENTY_FOUR_WELL_PLATE.get_well_name_from_well_index(well_index)
            msg = f"Writing waveform data of well {well_name} ({iter_well_idx + 1} out of {num_wells})"
            logger.info(msg)

            # finding last index in interpolated data indices
            last_index = len(interpolated_data_indices) - 1
            first_index = 0

            # decrementing the last index marker until the last time point in filtered_data is greater than the value of interpolated_data_indices at the last index
            while filtered_data[0][-1] < interpolated_data_indices[last_index]:
                last_index -= 1

            # incrementing last_index so the previously found index value less than the last filtered_data timepoint is included in the interpolate function and represnts the correct number of data points
            last_index += 1

            while filtered_data[0][0] > interpolated_data_indices[first_index]:
                first_index += 1

            interpolated_data = interpolated_data_function(
                interpolated_data_indices[first_index:last_index]
            )

            # write to sheet
            for i, data_point in enumerate(interpolated_data):
                curr_sheet.write(i + 1, well_index + 1, data_point)
            self._create_waveform_charts(
                skip_charts,
                iter_well_idx,
                last_index,
                well_index,
                well_name,
                filtered_data[0],
                interpolated_data_function,
            )

        # The formatting items below are not explicitly unit-tested...not sure the best way to do this
        # Adjust the column widths to be able to see the data
        curr_sheet.set_column(0, 0, 18)
        well_indices = self.get_well_indices()
        for iter_well_idx in range(24):
            curr_sheet.set_column(
                iter_well_idx + 1,
                iter_well_idx + 1,
                13,
                options={"hidden": iter_well_idx not in well_indices},
            )
        curr_sheet.freeze_panes(1, 1)

    # pylint: disable=too-many-locals
    def _create_waveform_charts(
        self,
        skip_charts: bool,
        iter_well_idx: int,
        num_data_points: int,
        well_index: int,
        well_name: str,
        time_values: NDArray[(2, Any), int],
        interpolated_data_function: interpolate.interpolate.interp1d,
    ) -> None:
        snapshot_chart_sheet = self._workbook.get_worksheet_by_name(
            SNAPSHOT_CHART_SHEET_NAME
        )
        full_chart_sheet = self._workbook.get_worksheet_by_name(FULL_CHART_SHEET_NAME)

        msg = f"Creating chart of waveform data of well {well_name}"
        logger.info(msg)
        snapshot_chart = None
        full_chart = None
        if not skip_charts:
            snapshot_chart = self._workbook.add_chart(
                {"type": "scatter", "subtype": "straight"}
            )
            full_chart = self._workbook.add_chart(
                {"type": "scatter", "subtype": "straight"}
            )
        well_column = xl_col_to_name(well_index + 1)
        recording_stop_time = time_values[-1] // CENTIMILLISECONDS_PER_SECOND
        lower_x_bound = (
            0
            if recording_stop_time <= CHART_WINDOW_NUM_SECONDS
            else int((recording_stop_time - CHART_WINDOW_NUM_SECONDS) // 2)
        )
        upper_x_bound = (
            recording_stop_time
            if recording_stop_time <= CHART_WINDOW_NUM_SECONDS
            else int((recording_stop_time + CHART_WINDOW_NUM_SECONDS) // 2)
        )
        msg = f"Adding peak and valley markers to chart of well {well_name}"
        logger.info(msg)
        for chart, chart_sheet in (
            (snapshot_chart, snapshot_chart_sheet),
            (full_chart, full_chart_sheet),
        ):
            if (
                chart is not None
            ):  # Tanner (11/11/20): chart is None when skipping chart creation
                chart.add_series(
                    {
                        "name": "Waveform Data",
                        "categories": f"='continuous-waveforms'!$A$2:$A${num_data_points}",
                        "values": f"='continuous-waveforms'!${well_column}$2:${well_column}${num_data_points}",
                        "line": {"color": "#1B9E77"},
                    }
                )

            peak_indices, valley_indices = self._pipelines[
                well_index
            ].get_peak_detection_results()
            self._add_peak_detection_series(
                chart,
                "Peak",
                well_index,
                well_name,
                num_data_points,
                peak_indices,
                interpolated_data_function,
                time_values,
            )
            self._add_peak_detection_series(
                chart,
                "Valley",
                well_index,
                well_name,
                num_data_points,
                valley_indices,
                interpolated_data_function,
                time_values,
            )

            if (
                chart is None
            ):  # Tanner (11/11/20): chart is None when skipping chart creation
                continue

            (
                well_row,
                well_col,
            ) = TWENTY_FOUR_WELL_PLATE.get_row_and_column_from_well_index(well_index)
            x_axis_settings: Dict[str, Any] = {"name": "Time (seconds)"}
            if chart == snapshot_chart:
                x_axis_settings["min"] = lower_x_bound
                x_axis_settings["max"] = upper_x_bound
            else:
                x_axis_settings["min"] = 0
                x_axis_settings["max"] = recording_stop_time
            chart.set_x_axis(x_axis_settings)
            y_axis_label = (
                "Post Displacement (microns)"
                if self._is_optical_recording
                else "Magnetic Sensor Data"
            )
            chart.set_y_axis({"name": y_axis_label, "major_gridlines": {"visible": 0}})
            width = (
                CHART_FIXED_WIDTH
                if chart == snapshot_chart
                else CHART_FIXED_WIDTH // 2
                + (DEFAULT_CELL_WIDTH * int(recording_stop_time / SECONDS_PER_CELL))
            )
            chart.set_size({"width": width, "height": CHART_HEIGHT})
            chart.set_title({"name": f"Well {well_name}"})
            if chart == snapshot_chart:
                chart_sheet.insert_chart(
                    1 + well_row * (CHART_HEIGHT_CELLS + 1),
                    1 + well_col * (CHART_FIXED_WIDTH_CELLS + 1),
                    chart,
                )
            else:
                chart_sheet.insert_chart(
                    1 + iter_well_idx * (CHART_HEIGHT_CELLS + 1),
                    1,
                    chart,
                )

    def _add_peak_detection_series(
        self,
        waveform_chart: xlsxwriter.chart_scatter.ChartScatter,
        detector_type: str,
        well_index: int,
        well_name: str,
        upper_x_bound_cell: int,
        indices: NDArray[(1, Any), int],
        interpolated_data_function: interpolate.interpolate.interp1d,
        time_values: NDArray[(2, Any), int],
    ) -> None:
        label = "Relaxation" if detector_type == "Valley" else "Contraction"
        offset = 1 if detector_type == "Valley" else 0
        marker_color = "#D95F02" if detector_type == "Valley" else "#7570B3"
        continuous_waveform_sheet = self._workbook.get_worksheet_by_name(
            CONTINUOUS_WAVEFORM_SHEET_NAME
        )
        result_column = xl_col_to_name(
            PEAK_VALLEY_COLUMN_START + (well_index * 2) + offset
        )
        continuous_waveform_sheet.write(
            f"{result_column}1", f"{well_name} {detector_type} Values"
        )
        for idx in indices:
            uninterpolated_time_seconds = round(
                time_values[idx] / CENTIMILLISECONDS_PER_SECOND, 2
            )
            row = (
                int(
                    uninterpolated_time_seconds
                    * CENTIMILLISECONDS_PER_SECOND
                    / self._interpolated_data_period
                )
                if self._is_optical_recording
                else uninterpolated_time_seconds
                * int(1 / INTERPOLATED_DATA_PERIOD_SECONDS)
                + 1
            )
            value = interpolated_data_function(
                uninterpolated_time_seconds * CENTIMILLISECONDS_PER_SECOND
            )
            continuous_waveform_sheet.write(f"{result_column}{row}", value)
        if (
            waveform_chart is not None
        ):  # Tanner (11/11/20): chart is None when skipping chart creation
            waveform_chart.add_series(
                {
                    "name": label,
                    "categories": f"='continuous-waveforms'!$A$2:$A${upper_x_bound_cell}",
                    "values": f"='continuous-waveforms'!${result_column}$2:${result_column}${upper_x_bound_cell}",
                    "marker": {
                        "type": "circle",
                        "size": 8,
                        "border": {"color": marker_color, "width": 1.5},
                        "fill": {"none": True},
                    },
                    "line": {"none": True},
                }
            )

    def _write_xlsx_per_twitch_metrics(self) -> None:
        logger.info("Creating per-twitch metrics sheet")
        curr_sheet = self._workbook.add_worksheet(PER_TWITCH_METRICS_SHEET_NAME)

        self._workbook.add_worksheet(TWITCH_FREQUENCIES_CHART_SHEET_NAME)
        self._workbook.add_worksheet(FORCE_FREQUENCY_RELATIONSHIP_SHEET)

        curr_row = 0
        well_indices = self.get_well_indices()

        for iter_well_idx in range(
            TWENTY_FOUR_WELL_PLATE.row_count * TWENTY_FOUR_WELL_PLATE.column_count
        ):
            well_name = TWENTY_FOUR_WELL_PLATE.get_well_name_from_well_index(
                iter_well_idx
            )
            curr_sheet.write(
                curr_row,
                0,
                well_name,
            )
            if iter_well_idx in well_indices:
                iter_pipeline = self._pipelines[iter_well_idx]
                error_msg = ""
                try:
                    (
                        per_twitch_dict,
                        aggregate_metrics_dict,
                    ) = iter_pipeline.get_magnetic_data_metrics()
                except PeakDetectionError as e:
                    error_msg = "Error: "
                    if isinstance(e, TwoPeaksInARowError):
                        error_msg += "Two Contractions in a Row Detected"
                    elif isinstance(e, TwoValleysInARowError):
                        error_msg += "Two Relaxations in a Row Detected"
                    elif isinstance(e, TooFewPeaksDetectedError):
                        error_msg += "Not Enough Twitches Detected"
                    else:
                        raise NotImplementedError("Unknown PeakDetectionError") from e
                    curr_sheet.write(curr_row, 1, "N/A")
                    curr_sheet.write(curr_row + 1, 1, error_msg)
                else:
                    number_twitches = aggregate_metrics_dict[AMPLITUDE_UUID]["n"]

                    curr_row = _write_per_twitch_metric_values(
                        curr_sheet, curr_row, per_twitch_dict, number_twitches
                    )

                    twitch_timepoints = list(per_twitch_dict)

                    self._create_frequency_vs_time_charts(
                        iter_well_idx,
                        well_name,
                        number_twitches,
                        twitch_timepoints,
                    )

                    self._create_force_frequency_relationship_charts(
                        iter_well_idx,
                        well_name,
                        number_twitches,
                    )

            curr_row += 1
            curr_sheet.write(
                curr_row,
                0,
                "Timepoint of Twitch Contraction",
            )
            curr_row += 1
            curr_row = _write_per_twitch_metric_labels(curr_sheet, curr_row)

            curr_row += (
                NUMBER_OF_PER_TWITCH_METRICS + 1 - 8
            )  # include a single row gap in between the data for each well

    def _create_force_frequency_relationship_charts(
        self,
        well_index: int,
        well_name: str,
        num_data_points: int,
    ) -> None:
        force_frequency_sheet = self._workbook.get_worksheet_by_name(
            FORCE_FREQUENCY_RELATIONSHIP_SHEET
        )

        msg = f"Creating chart of force-frequency data of well {well_name}"
        logger.info(msg)

        force_frequency_chart = self._workbook.add_chart({"type": "scatter"})

        well_row = well_index * (NUMBER_OF_PER_TWITCH_METRICS + 2)
        last_column = xl_col_to_name(num_data_points)

        force_frequency_chart.add_series(
            {
                "categories": f"='{PER_TWITCH_METRICS_SHEET_NAME}'!$B${well_row + 4}:${last_column}${well_row + 4}",
                "values": f"='{PER_TWITCH_METRICS_SHEET_NAME}'!$B${well_row + 5}:${last_column}${well_row + 5}",
            }
        )

        force_frequency_chart.set_legend({"none": True})

        x_axis_label = CALCULATED_METRIC_DISPLAY_NAMES[TWITCH_FREQUENCY_UUID]

        force_frequency_chart.set_x_axis({"name": x_axis_label})

        y_axis_label = CALCULATED_METRIC_DISPLAY_NAMES[AMPLITUDE_UUID]

        force_frequency_chart.set_y_axis(
            {"name": y_axis_label, "major_gridlines": {"visible": 0}}
        )

        force_frequency_chart.set_size(
            {"width": CHART_FIXED_WIDTH, "height": CHART_HEIGHT}
        )
        force_frequency_chart.set_title({"name": f"Well {well_name}"})

        well_row, well_col = TWENTY_FOUR_WELL_PLATE.get_row_and_column_from_well_index(
            well_index
        )

        force_frequency_sheet.insert_chart(
            1 + well_row * (CHART_HEIGHT_CELLS + 1),
            1 + well_col * (CHART_FIXED_WIDTH_CELLS + 1),
            force_frequency_chart,
        )

    def _create_frequency_vs_time_charts(
        self,
        well_index: int,
        well_name: str,
        num_data_points: int,
        time_values: NDArray[(1, Any), int],
    ) -> None:
        frequency_chart_sheet = self._workbook.get_worksheet_by_name(
            TWITCH_FREQUENCIES_CHART_SHEET_NAME
        )

        msg = f"Creating chart of frequency data of well {well_name}"
        logger.info(msg)

        frequency_chart = self._workbook.add_chart({"type": "scatter"})

        well_row = well_index * (NUMBER_OF_PER_TWITCH_METRICS + 2)
        last_column = xl_col_to_name(num_data_points)

        frequency_chart.add_series(
            {
                "categories": f"='{PER_TWITCH_METRICS_SHEET_NAME}'!$B${well_row + 2}:${last_column}${well_row + 2}",
                "values": f"='{PER_TWITCH_METRICS_SHEET_NAME}'!$B${well_row + 4}:${last_column}${well_row + 4}",
            }
        )

        frequency_chart.set_legend({"none": True})

        x_axis_settings: Dict[str, Any] = {"name": "Time (seconds)"}
        x_axis_settings["min"] = 0
        x_axis_settings["max"] = time_values[-1] // CENTIMILLISECONDS_PER_SECOND

        frequency_chart.set_x_axis(x_axis_settings)

        y_axis_label = CALCULATED_METRIC_DISPLAY_NAMES[TWITCH_FREQUENCY_UUID]

        frequency_chart.set_y_axis(
            {"name": y_axis_label, "min": 0, "major_gridlines": {"visible": 0}}
        )

        frequency_chart.set_size({"width": CHART_FIXED_WIDTH, "height": CHART_HEIGHT})
        frequency_chart.set_title({"name": f"Well {well_name}"})

        well_row, well_col = TWENTY_FOUR_WELL_PLATE.get_row_and_column_from_well_index(
            well_index
        )

        frequency_chart_sheet.insert_chart(
            1 + well_row * (CHART_HEIGHT_CELLS + 1),
            1 + well_col * (CHART_FIXED_WIDTH_CELLS + 1),
            frequency_chart,
        )

    def _write_xlsx_aggregate_metrics(self) -> None:
        logger.info("Creating aggregate metrics sheet")
        curr_sheet = self._workbook.add_worksheet(AGGREGATE_METRICS_SHEET_NAME)
        curr_row = 0
        for iter_well_idx in range(
            TWENTY_FOUR_WELL_PLATE.row_count * TWENTY_FOUR_WELL_PLATE.column_count
        ):
            curr_sheet.write(
                curr_row,
                2 + iter_well_idx,
                TWENTY_FOUR_WELL_PLATE.get_well_name_from_well_index(iter_well_idx),
            )
        curr_row += 1
        curr_sheet.write(curr_row, 1, "Treatment Description")
        curr_row += 1
        curr_sheet.write(curr_row, 1, "n (twitches)")
        well_indices = self.get_well_indices()
        for iter_well_idx in well_indices:
            iter_pipeline = self._pipelines[iter_well_idx]
            error_msg = ""
            try:
                _, aggregate_metrics_dict = iter_pipeline.get_magnetic_data_metrics()
            except PeakDetectionError as e:
                error_msg = "Error: "
                if isinstance(e, TwoPeaksInARowError):
                    error_msg += "Two Contractions in a Row Detected"
                elif isinstance(e, TwoValleysInARowError):
                    error_msg += "Two Relaxations in a Row Detected"
                elif isinstance(e, TooFewPeaksDetectedError):
                    error_msg += "Not Enough Twitches Detected"
                else:
                    raise NotImplementedError("Unknown PeakDetectionError") from e
                curr_sheet.write(curr_row, 2 + iter_well_idx, "N/A")
                curr_sheet.write(curr_row + 1, 2 + iter_well_idx, error_msg)
            else:
                curr_sheet.write(
                    curr_row,
                    2 + iter_well_idx,
                    aggregate_metrics_dict[AMPLITUDE_UUID]["n"],
                )

        curr_row += 1
        # row_where_data_starts=curr_row
        for (
            iter_metric_uuid,
            iter_metric_name,
        ) in CALCULATED_METRIC_DISPLAY_NAMES.items():
            curr_row += 1
            new_row = self._write_submetrics(
                curr_sheet,
                curr_row,
                iter_metric_uuid,
                iter_metric_name,
            )
            curr_row = new_row

        # The formatting items below are not explicitly unit-tested...not sure the best way to do this
        # Adjust the column widths to be able to see the data
        for iter_column_idx, iter_column_width in ((0, 40), (1, 25)):
            curr_sheet.set_column(iter_column_idx, iter_column_idx, iter_column_width)
        # adjust widths of well columns
        for iter_column_idx in range(24):
            curr_sheet.set_column(
                iter_column_idx + 2,
                iter_column_idx + 2,
                19,
                options={"hidden": iter_column_idx not in well_indices},
            )
        curr_sheet.freeze_panes(2, 2)

    def _write_submetrics(
        self,
        curr_sheet: xlsxwriter.worksheet.Worksheet,
        curr_row: int,
        iter_metric_uuid: uuid.UUID,
        iter_metric_name: Union[str, Tuple[int, str]],
    ) -> int:
        submetrics = ("Mean", "StDev", "CoV", "SEM")
        if isinstance(iter_metric_name, tuple):
            iter_width_percent, iter_metric_name = iter_metric_name
        curr_sheet.write(curr_row, 0, iter_metric_name)
        for iter_sub_metric_name in submetrics:
            msg = f"Writing {iter_sub_metric_name} of {iter_metric_name}"
            logger.info(msg)
            curr_sheet.write(curr_row, 1, iter_sub_metric_name)
            well_indices = self.get_well_indices()
            for well_index in well_indices:
                value_to_write: Optional[Union[float, int, str]] = None
                cell_format: Optional[Format] = None
                iter_pipeline = self._pipelines[well_index]

                try:
                    (
                        _,
                        aggregate_metrics_dict,
                    ) = iter_pipeline.get_magnetic_data_metrics()
                except PeakDetectionError:
                    value_to_write = "N/A"
                else:
                    metrics_dict = dict()
                    if iter_metric_uuid == WIDTH_UUID:
                        metrics_dict = aggregate_metrics_dict[iter_metric_uuid][
                            iter_width_percent
                        ]
                    else:
                        metrics_dict = aggregate_metrics_dict[iter_metric_uuid]
                    if iter_sub_metric_name == "Mean":
                        value_to_write = metrics_dict["mean"]
                    elif iter_sub_metric_name == "StDev":
                        value_to_write = metrics_dict["std"]
                    elif iter_sub_metric_name == "CoV":
                        value_to_write = metrics_dict["std"] / metrics_dict["mean"]
                        cell_format = self._workbook_formats["CoV"]
                    elif iter_sub_metric_name == "SEM":
                        value_to_write = metrics_dict["std"] / metrics_dict["n"] ** 0.5
                    else:
                        raise NotImplementedError(
                            f"Unrecognized submetric name: {iter_sub_metric_name}"
                        )

                    if iter_metric_uuid in (
                        TWITCH_PERIOD_UUID,
                        WIDTH_UUID,
                    ):  # for time-based metrics, convert from centi-milliseconds to seconds before writing to Excel
                        if (
                            iter_sub_metric_name != "CoV"
                        ):  # coefficients of variation are %, not a raw time unit
                            value_to_write /= CENTIMILLISECONDS_PER_SECOND
                    if iter_metric_uuid in (
                        CONTRACTION_VELOCITY_UUID,
                        RELAXATION_VELOCITY_UUID,
                    ):  # for velocity-based metrics, convert from centi-milliseconds to seconds before writing to Excel
                        if (
                            iter_sub_metric_name != "CoV"
                        ):  # coefficients of variation are %, not a raw time unit
                            value_to_write *= CENTIMILLISECONDS_PER_SECOND
                curr_sheet.write(curr_row, 2 + well_index, value_to_write, cell_format)

            curr_row += 1
        return curr_row
