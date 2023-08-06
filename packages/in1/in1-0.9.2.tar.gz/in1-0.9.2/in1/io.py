from typing import Union, Tuple
import warnings

import numpy as np
import rasterio as rio
import rasterio.profiles as riop
from requests import Response


def read(raster_path: str) -> Union[np.ndarray, riop.Profile]:
    """Loads a georeferenced image with rasterio.

    Parameters
    ----------
    raster_path: str
        Path to the image to load.

    Returns
    -------
    Union[numpy.ndarray, rasterio.profiles.Profile]
        A tuple containing the image and metadata. The first tuple item is the image
        as a numpy array shaped [C, H, W]. The second item is a rasterio profile
        class, which contains the georeferencing and file format options.
    """
    with rio.open(raster_path) as handle:
        image = handle.read()
        profile = handle.profile
    return image, profile


def write(raster: np.ndarray, raster_path: str, profile: Union[dict, riop.Profile]):
    """Write raster to file.

    Parameters
    ----------
    raster: numpy.ndarray
        The numpy raster to write out, shaped [C, H, W].
    raster_path: str
        The filepath to write to.
    profile: Union[dict, rasterio.profiles.Profile]
        The rasterio profile to use for writing to a file. Modify these key-values to
        change file format options.
    """
    count, height, width = raster.shape
    profile = profile.copy()  # Copy to prevent changing a var caller has reference to
    profile.update(count=count, height=height, width=width, dtype=raster.dtype)

    with rio.open(raster_path, "w", **profile) as handle:
        handle.write(raster)


def to_memory(raster: np.ndarray) -> rio.MemoryFile:
    """Writes a raster to memory (byte format).

    Parameters
    ----------
    raster: np.ndarray
        The numpy raster to write to memory, shaped [C, H, W].

    Returns
    -------
    rasterio.MemorFile
    """
    profile = {
        "driver": "GTiff",
        "count": raster.shape[0],
        "height": raster.shape[1],
        "width": raster.shape[2],
        "dtype": raster.dtype,
    }

    memfile = rio.MemoryFile()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with memfile.open(**profile) as handle:
            handle.write(raster)
            handle.close()
    return memfile
