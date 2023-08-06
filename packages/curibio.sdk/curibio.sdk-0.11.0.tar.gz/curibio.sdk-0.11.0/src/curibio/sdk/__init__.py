# -*- coding: utf-8 -*-
"""Docstring."""

from mantarray_file_manager import WellFile

from . import jupyter_helpers
from .constants import AGGREGATE_METRICS_SHEET_NAME
from .constants import ALL_FORMATS
from .constants import CALCULATED_METRIC_DISPLAY_NAMES
from .constants import CHART_BASE_WIDTH
from .constants import CHART_FIXED_WIDTH
from .constants import CHART_FIXED_WIDTH_CELLS
from .constants import CHART_HEIGHT
from .constants import CHART_HEIGHT_CELLS
from .constants import CHART_WINDOW_NUM_DATA_POINTS
from .constants import CHART_WINDOW_NUM_SECONDS
from .constants import CONTINUOUS_WAVEFORM_SHEET_NAME
from .constants import DEFAULT_CELL_WIDTH
from .constants import EXCEL_OPTICAL_METADATA_CELLS
from .constants import FORCE_FREQUENCY_RELATIONSHIP_SHEET
from .constants import FULL_CHART_SHEET_NAME
from .constants import INTERPOLATED_DATA_PERIOD_CMS
from .constants import INTERPOLATED_DATA_PERIOD_SECONDS
from .constants import INTERPOLATION_VALUE_UUID
from .constants import METADATA_EXCEL_SHEET_NAME
from .constants import METADATA_INSTRUMENT_ROW_START
from .constants import METADATA_OUTPUT_FILE_ROW_START
from .constants import METADATA_RECORDING_ROW_START
from .constants import METADATA_UUID_DESCRIPTIONS
from .constants import MICROSECONDS_PER_CENTIMILLISECOND
from .constants import NUMBER_OF_PER_TWITCH_METRICS
from .constants import PACKAGE_VERSION as __version__
from .constants import PEAK_VALLEY_COLUMN_START
from .constants import PER_TWITCH_METRICS_SHEET_NAME
from .constants import SECONDS_PER_CELL
from .constants import SNAPSHOT_CHART_SHEET_NAME
from .constants import TSP_TO_DEFAULT_FILTER_UUID
from .constants import TWITCH_FREQUENCIES_CHART_SHEET_NAME
from .constants import TWITCHES_POINT_UP_UUID
from .excel_well_file import ExcelWellFile
from .exceptions import MetadataNotFoundError
from .jupyter_helpers import check_if_latest_version
from .jupyter_helpers import get_latest_version_from_pypi
from .plate_recording import PlateRecording

__all__ = [
    "WellFile",
    "ExcelWellFile",
    "PlateRecording",
    "check_if_latest_version",
    "get_latest_version_from_pypi",
    "jupyter_helpers",
    "METADATA_EXCEL_SHEET_NAME",
    "METADATA_RECORDING_ROW_START",
    "METADATA_INSTRUMENT_ROW_START",
    "METADATA_OUTPUT_FILE_ROW_START",
    "CONTINUOUS_WAVEFORM_SHEET_NAME",
    "INTERPOLATED_DATA_PERIOD_CMS",
    "TSP_TO_DEFAULT_FILTER_UUID",
    "MICROSECONDS_PER_CENTIMILLISECOND",
    "CALCULATED_METRIC_DISPLAY_NAMES",
    "AGGREGATE_METRICS_SHEET_NAME",
    "ALL_FORMATS",
    "__version__",
    "SNAPSHOT_CHART_SHEET_NAME",
    "CHART_HEIGHT",
    "CHART_BASE_WIDTH",
    "CHART_HEIGHT_CELLS",
    "PEAK_VALLEY_COLUMN_START",
    "DEFAULT_CELL_WIDTH",
    "CHART_FIXED_WIDTH",
    "CHART_FIXED_WIDTH_CELLS",
    "INTERPOLATED_DATA_PERIOD_SECONDS",
    "CHART_WINDOW_NUM_SECONDS",
    "CHART_WINDOW_NUM_DATA_POINTS",
    "EXCEL_OPTICAL_METADATA_CELLS",
    "TWITCHES_POINT_UP_UUID",
    "METADATA_UUID_DESCRIPTIONS",
    "MetadataNotFoundError",
    "INTERPOLATION_VALUE_UUID",
    "FULL_CHART_SHEET_NAME",
    "SECONDS_PER_CELL",
    "PER_TWITCH_METRICS_SHEET_NAME",
    "NUMBER_OF_PER_TWITCH_METRICS",
    "TWITCH_FREQUENCIES_CHART_SHEET_NAME",
    "FORCE_FREQUENCY_RELATIONSHIP_SHEET",
]
