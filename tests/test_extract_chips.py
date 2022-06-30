import pytest
import os
import tempfile
import sys
from pathlib import Path
import numpy as np
from raster_analysis.extract_chips import get_tif_files, extract_chips_multi_point


geo_json = "./tests/test_data/test_raster/test_coordinates.geojson"
raster_dir = "./tests/test_data/test_raster/"
chip_size = 5
test_coordinate = (-74.79528902505427, 40.946807786177864)


def test_get_tif_files_returns_3_files():
    test_file_dir = "./tests/test_data/text_files"
    test_list_of_files = get_tif_files(test_file_dir, ["txt"])
    assert len(test_list_of_files) == 3


def test_get_tif_files_returns_1_files():
    test_file_dir = "./tests/test_data/test_raster"
    test_list_of_files = get_tif_files(test_file_dir, ["tif"])
    assert len(test_list_of_files) == 1


def test_extract_chips_len_two_for_two_coordinates():
    test_run = extract_chips_multi_point(geo_json, raster_dir, chip_size)
    assert len(test_run) == 2


def test_extract_chips_is_list():
    test_run = extract_chips_multi_point(geo_json, raster_dir, chip_size)
    assert type(test_run[test_coordinate]) == list


def test_extract_chips_returns_array():
    test_run = extract_chips_multi_point(geo_json, raster_dir, chip_size)
    assert type(test_run[test_coordinate][0]) == np.ndarray


def test_extract_chips_returns_array_with_proper_shape():
    test_run = extract_chips_multi_point(geo_json, raster_dir, chip_size)
    assert test_run[test_coordinate][0].shape == (6, 11, 11)
