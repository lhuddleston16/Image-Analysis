import rasterio
import json
import os
from pathlib import Path
import numpy as np
import re


# python -m raster_analysis.extract_chips

def validate_file_pathname(
    pathname: str,
    is_file: bool,
    allowed_extensions: list = [],
    max_pathname_length: int = 140,
):
    """Raises exception if file pathname is invalid.

    Args:
        pathname (str): pathname to file
        is_file (bool): Mark True if the path should be a file
        allowed_extensions (list): List of extensions allowed. Defaults to empty list.
        max_pathname_length (int): Max number of characters in path. Defaults to 140
    """
    if os.path.isabs(pathname):
        raise ValueError(f"File path is absolute and needs to be relative: {pathname}")

    if len(pathname) > max_pathname_length:
        raise ValueError(f"Pathname length exceeds {max_pathname_length} characters")
    special_char_regex = re.compile(r"[@ !#$%^&*()<>?\|}{~:]")
    if special_char_regex.search(pathname):
        raise ValueError(
            r"Characters [@ !#$%^&*()<>?\|}{~:] not allowed:" f"{pathname}"
        )
    if len(allowed_extensions) > 0 and is_file:
        if pathname.rpartition(".")[2] not in allowed_extensions:
            raise ValueError(
                f"File type must be one of {allowed_extensions}: {pathname}"
            )
    if not os.path.exists(pathname):
        raise FileNotFoundError(f"File path does not exist: {pathname}")

    if os.path.isdir(pathname) and is_file:
        raise ValueError(f"File path is a directory and needs to be a file: {pathname}")

def get_tif_files(raster_dir: str, allowed_extensions: list):
    """Get all files in directory that match allowed_extensions.

    Args:
        dir (str): a directory. Path needs to be relative.
        allowed_extensions (list): List of extensions allowed. Defaults to empty list.
    Returns:
        List: A list of .tif files
    """
    tif_files = []
    for file in os.listdir(raster_dir):
        if file.rpartition(".")[2] in allowed_extensions:
            pathname = os.path.join(raster_dir, file)
            validate_file_pathname(
                pathname=pathname,
                is_file=True,
                allowed_extensions=allowed_extensions,
                max_pathname_length=140,
            )
            tif_files.append(pathname)
    return tif_files


def extract_chips_multi_point(
    coordinates_geojson_path: str, raster_dir: str, chip_size: int
):
    """This function extracts chips from a raster file based on the coordinates in the geojson file and the chip size.

    Args:
        coordinates_geojson_path (str): path to a local GeoJSON file containing coordinate data. Path needs to be relative.
        raster_dir (str): a directory containing GeoTIFF files with filenames formatted like {X}_{Y}_{zoom}.tif. Path needs to be relative.
        chip_size (int): padding level around the pixel corresponding to a particular coordinate.
    Return:
        Dictionary: A dictionary where each key corresponds to a coordinate with a value being a list of chips, one per year. Each chip is a numpy array of shape [6, 2*chip_size + 1, 2*chip_size + 1]

    """
    tif_files = get_tif_files(raster_dir, ["tif"])

    output_coords_with_chips = {}
    # Open the coordinates file
    with open(coordinates_geojson_path) as f:
        shapes = json.load(f)
    for tif_file in tif_files:
        # Parse pathfile to get stem for naming
        tif_file_name = Path(tif_file).stem
        # Open the raster
        with rasterio.open(tif_file) as dataset:
            # Loop the list of coordinates
            for count, coordinate in enumerate(shapes["coordinates"]):
                # Get pixel values from coordinates
                py, px = dataset.index(coordinate[0], coordinate[1])

                # Create an chip_size by chip_size window
                window = rasterio.windows.Window(
                    px, py, 2 * chip_size + 1, 2 * chip_size + 1
                )

                # Get the data from the window
                clip = dataset.read(window=window)
                clip_not_empty = clip.nonzero()[0].any()

                # Assuming all coordinates should live in the raster files so I am not appending empty arrays
                if clip_not_empty == True:
                    # Reshape data based on year
                    output_coords_with_chips[tuple(coordinate)] = np.array_split(
                        clip, 37
                    )
    return output_coords_with_chips


if __name__ == "__main__":
    geo_json = "./tests/test_data/test_raster/test_coordinates.geojson"
    raster_dir = "./tests/test_data/test_raster/"
    chip_size = 4
    test_run = extract_chips_multi_point(geo_json, raster_dir, chip_size)
    test_coordinate = (-74.79528902505427, 40.946807786177864)
    print(f"Type of object returned: {type(test_run)}")
    print(f"Type of object in dictionary: {type(test_run[test_coordinate])}")
    print(f"Length of list: {len(test_run[test_coordinate])}")
    print(f"Type item in list: {type(test_run[test_coordinate][0])}")
    print(f"Shape array in list: {test_run[test_coordinate][0].shape}")
