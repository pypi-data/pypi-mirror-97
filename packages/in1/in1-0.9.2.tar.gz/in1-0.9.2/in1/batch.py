from typing import Union, Callable
import os
import numpy as np
import warnings

import tqdm
import rasterio as rio
from rasterio.windows import Window

import in1
import in1.io
import in1.exceptions as in1e


def process_batch(
    raster: Union[str, np.ndarray, rio.MemoryFile],
    operation: Callable[[bytes], bytes],
    calc_metrics: bool,
) -> rio.MemoryFile:
    """Applies an operation to a raster in batched fashion.

    This function tiles its input, each tile being a batch item, to support processing
    large files.

    Arguments
    ---------
    raster: Union[str, np.ndarray, rio.MemoryFile]
        The source raster to operate upon. Can be a filepath, a numpy raster shaped
        [C, H, W], or a rasterio MemoryFile.
    operation: Callable[[bytes], bytes]
        The operation the batch processor should apply. This is expected to be the
        `inference.infer` function with all its paramters filled, except for the
        raster parameter. The batch processor will read tiles from its own raster,
        convert such a tile to bytes, which the infer function will then send to the
        server.
    calc_metrics: bool
        Set to true if the operation returns metrics as well. The batch processor needs
        this to know so it can

    Returns
    -------
    A rasterio MemoryFile with the result raster.
    """
    # Define constants
    overlap = 10
    tiles_size = 108
    up_factor = 4

    # Depending on the given parameter, load the right kind of file
    if isinstance(raster, str):
        src = rio.open(raster)
    elif isinstance(raster, np.ndarray):
        src_memfile = in1.io.to_memory(raster)
        src = src_memfile.open()
    elif isinstance(raster, rio.MemoryFile):
        src = raster.open()
    else:
        t = type(raster)
        raise ValueError(f"Unsupported input type for source raster {t}")

    # Using the source raster, apply the operation
    # Get new transform for final raster profile and update result raster profile
    dst_profile = src.profile.copy()
    c = 1 / up_factor
    dst_transform = src.profile["transform"] * src.profile["transform"].scale(c, c)
    dst_profile.update(
        {
            "transform": dst_transform,
            "count": src.profile["count"] + 2 if calc_metrics else src.profile["count"],
            "height": src.profile["height"] * up_factor,
            "width": src.profile["width"] * up_factor,
            "driver": "GTiff",
            "crs": src.profile["crs"],
        }
    )

    # Scan a window across the raster's source and destination, reading overlapping tiles,
    # applying the operation and writing non-overlapping parts to file.
    destination = rio.MemoryFile()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with destination.open(**dst_profile) as dst:
            # Add extra tile_size to make sure range goes over raster edges
            max_width = src.width
            max_height = src.height
            steps_x = range(0, max_width + tiles_size, tiles_size)
            steps_y = range(0, max_height + tiles_size, tiles_size)

            total = int((max_height + tiles_size) / tiles_size) + 1
            total *= int((max_width + tiles_size) / tiles_size) + 1

            boxes = ((x, y) for x in steps_x for y in steps_y)
            for (x, y) in tqdm.tqdm(boxes, total=total):
                # Determine tiles coordinates and size to read
                tile_x = x - overlap
                tile_y = y - overlap
                tile_width = tiles_size + 2 * overlap
                tile_height = tiles_size + 2 * overlap

                # Ensure x and Y to read fall within raster [0, max_x or max_y]
                tile_x = max(min(tile_x, max_width), 0)
                tile_y = max(min(tile_y, max_height), 0)

                # Read tile and skip empty results
                tile = src.read(window=Window(tile_x, tile_y, tile_width, tile_height))
                if 0 in list(tile.shape):
                    continue

                # Apply
                try:
                    tile_bytes = in1.io.to_memory(tile).read()
                    result_bytes = operation(tile_bytes)
                    with rio.MemoryFile(result_bytes) as memf, memf.open() as dataset:
                        tile = dataset.read()

                    # Determine overlap and cut off if present
                    left_x = 0 if tile_x * up_factor == 0 else overlap * up_factor
                    right_x = left_x * up_factor + (tiles_size * up_factor)
                    top_y = 0 if tile_y * up_factor == 0 else overlap * up_factor
                    bottom_y = top_y * up_factor + (tiles_size * up_factor)
                    tile = tile[:, top_y:bottom_y, left_x:right_x]

                    # Write result. Correct x and y offsets for new upsample coordinates
                    x_write, y_write = x * up_factor, y * up_factor
                    window = Window(x_write, y_write, tile.shape[2], tile.shape[1])
                    dst.write(tile, window=window)
                except in1e.ServerError:
                    pass

    src.close()
    return destination
