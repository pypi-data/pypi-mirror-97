import os
from typing import Union, Tuple, Optional, Dict

import numpy as np
import rasterio as rio
from rasterio.profiles import Profile

from .batch import process_batch
from .inference import infer


def sisr(
    raster: Union[str, np.ndarray, rio.MemoryFile],
    api_key: str,
    calc_metrics: bool = True,
    host: str = "api.in1.ai",
    port: int = 80,
) -> Tuple[np.ndarray, Profile, Optional[Dict[str, np.ndarray]]]:
    """Takes an RGBI numpy array of shape [C, H, W] and queries the in1 service for a
    super sampled version of it, also of the shape [C, H, W].

    Parameters
    ----------
    raster_src: Union[str, numpy.ndarray]
         Either a filepath to an RGBI image or an RGBI numpy array shaped [C, H, W] of
         type uint16.
    api_key: str
        The token for authentication.
    calc_metrics: bool (Default: True)
        Whether or not to calculate additional metrics scoring the result's resolution
        and similarity to the original.
    host: str (Default: "api.in1.ai")
        Specify to override the host name to query (advanced).
    port: int (Default: 443)
        Specify to override the port to query on the host (advanced).

    Raises
    ------
    ValueError
        When `raster` is not a string to a file or not a numpy array.
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
    Tuple[np.ndarray, Profile, Optional[Dict[str, np.ndarray]]]
        A tuple containing the result raster, its rasterio profile, and optionally metric
        arrays as calculated by server.
            The first tuple element, the RGBI raster, is shaped [C, H, W]. The second
        element, the profile, is only complete if a this function was given a filepath. If
        it was given an array, georeferencing misses. If the given raster was a
        MemoryFile, the returned profile depends on what the MemoryFile contained.
            The third element, the metrics, is `None` if calc_metrics is `False`.
        Otherwise, it is a dictionary with fidelity & enhancement masks (np.ndarray with
        shapes are (1, H, W)) as values to provide quality measures that can be visualized
        for a given image.
    """
    # Construct the super resolvement operation using the infer function.
    # Its API parameters are populated with those given to by the user, and inferrence
    # is then applied by `batch.process_batch` to individual tiles.
    super_resolve = lambda batch_item: infer(
        raster=batch_item,
        api_key=api_key,
        calc_metrics=calc_metrics,
        host=host,
        port=port,
        endpoint="sentinel-2",
    )

    # Execute batched super resolving
    result = process_batch(raster, super_resolve, calc_metrics)

    # Read and return results
    with result.open() as handle:
        sisred = handle.read()
        profile = handle.profile.copy()

    metrics: Optional[Dict[str, np.ndarray]] = None
    if sisred.shape[0] > 4:
        fidelity = sisred[4:5, :, :]
        enhancement = sisred[5:6, :, :]
        metrics = {"fidelity": fidelity, "enhancement": enhancement}
        sisred = sisred[:4]
        profile.update(count=4)

    return sisred, profile, metrics
