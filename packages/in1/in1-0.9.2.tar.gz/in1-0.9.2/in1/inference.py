from typing import Union, Tuple, Dict, Optional

import numpy as np
import requests
from rasterio.profiles import Profile

from .exceptions import (
    NoResult,
    AuthenticationError,
    IncorrectImageGeneration,
    UnsupportedImageFormat,
    ServerError,
    InsufficientCredits,
)


def infer(
    raster: bytes,
    api_key: str,
    calc_metrics: bool,
    host: str,
    port: int,
    endpoint: str,
    version: int = 1,
) -> bytes:
    """Does the actual inference request.

    Parameters
    ----------
    raster: bytes
        The bytes of the file to send to the inference server.
    api_key: str
        The authentication token, for example the API key.
    calc_metrics: bool
        Whether or not to calculate additional metrics scoring the result's resolution
        and similarity to the original.
    host: str
        The host of the inference server.
    port: int
        The port the inference server listens on.
    endpoint: str
        Which endpoint to call.
    version: int (Default 1)
        Which API version to call.

    Raises
    ------
    requests.exceptions.ConnectionError
        If the server can't be reached.
    in1.exceptions.AuthenticationError
        For failure to authenticate the given api-key.
    in1.exceptions.IncorrectImageGeneration
        When the input image was incorrectly produced, resulting in malformed or
        corrupted image.
    in1.exceptions.UnsupportedImageFormat
        When the input image does not conform to format requirements (incl. image too
        large, incorrect order or number of dimensions).
    in1.exceptions.InsufficientCredits
        When insufficient credits are associated with the given account.
    in1.exceptions.ServerError
        For all issues arising on the server side.
    in1.exceptions.NoResultException
        When inference was not successful for unclear reasons.

    Returns
    -------
    bytes
        The bytes returned by the server which should contain a result raster.
    """
    rasters = {"submission": raster}
    qc = {True: "yes", False: "no"}
    headers = {"in1-api-key": api_key, "in1-calc-metrics": qc.get(calc_metrics, "yes")}

    target = f"http://{host}:{port}/v{version}/{endpoint}"
    response = requests.post(target, headers=headers, files=rasters)

    # Error handling given response status code
    if not response.ok:
        error: str = "Reason unspecified"

        try:
            error = response.json()["detail"]
        except:
            try:
                error = response.content.decode("utf-8")
            except:
                pass

        if response.status_code == 401:
            raise AuthenticationError(error)

        elif response.status_code == 402:
            raise InsufficientCredits(error)

        elif response.status_code == 415:
            raise UnsupportedImageFormat(error)

        elif response.status_code == 422:
            raise IncorrectImageGeneration(error)

        elif response.status_code == 500:
            raise ServerError(error)

        else:
            raise NoResult(error)

    # Get high resolution image as bytes
    return response.content
