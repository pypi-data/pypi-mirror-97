# -*- coding: utf-8 -*-
"""Small helper functions for the Jupyter Notebook."""
import requests

from .constants import PACKAGE_VERSION


def get_latest_version_from_pypi() -> str:
    """Get the latest version of this package from PyPI.

    Based on https://stackoverflow.com/questions/17069428/how-to-get-the-latest-version-number-of-a-package-on-pypi?noredirect=1&lq=1
    """
    response_json = requests.get(
        "https://pypi.org/pypi/curibio.sdk/json"
    ).json()  # Eli (1/18/21): if the URL is invalid, then decoding the JSON raises an error, so no need to explicitly check for HTTP failure
    extracted_version = response_json["info"]["version"]
    if not isinstance(extracted_version, str):
        raise NotImplementedError(
            f"The extracted version should always be a string. It was {extracted_version}"
        )
    return extracted_version


def check_if_latest_version() -> None:
    """Check to see if the version running locally is the latest from PyPi.

    There appears to be possible edge cases if someone leaves a window
    open where the Notebook won't update to the latest release.
    """
    latest_version = get_latest_version_from_pypi()
    if latest_version != PACKAGE_VERSION:
        print(  # allow-print
            f"WARNING! You are not running the latest version of the SDK. You are running {PACKAGE_VERSION}, but {latest_version} is available. It is strongly recommended to close this window and re-open a new Jupyter Notebook to ensure you are using the latest version."
        )
