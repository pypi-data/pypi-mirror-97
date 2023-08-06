import os
import tarfile
import requests

from .exceptions import DownloadFailed


def download_s2_dataset(download_dir: str = ".") -> str:
    """ Download in1's free trial dataset, with prepared images ready for experimentation!
        The dataset contains thousands of images of a variety of contintents and land
        covers.

        A georeferenced index is provided as well with it, allowing easy selection of
        interesting areas. The columns of interest in the GeoDataFrame are
        path, geometry, longitude, latitude, continent, and landcover

        Parameters
        ----------
        download_dir: str
            The directory to download and extract the archive to.

        Returns
        -------
        str
            If the download succeeded, a string pointing to the index of the dataset is
            returned. This file can be opened with geopandas.
    """
    filename = "in1-s2-dataset.tar.gz"
    url = "https://in1-pub.s3.eu-central-1.amazonaws.com/"

    src = url + filename
    dst = os.path.join(download_dir, filename)
    response = requests.get(src, allow_redirects=True)

    if not response.ok:
        raise DownloadFailed(f"Could not download in1 Sentinel-2 dataset from {src}")

    with open(dst, "wb") as handle:
        handle.write(response.content)

    with tarfile.open(dst, "r") as archive:
        archive.extractall(download_dir)

    dataset_dir = os.path.join(download_dir, "in1-s2-dataset")
    return os.path.join(dataset_dir, "index.gpkg")
