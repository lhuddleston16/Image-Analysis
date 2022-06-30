import pytest
import os
import tempfile
import sys
from pathlib import Path
from utilities.validate_path import validate_file_pathname


@pytest.fixture
def temp_file():
    temp_file = tempfile.NamedTemporaryFile(suffix=".tif")
    return temp_file


def test_directory_as_source_raises_exception_with_is_file_true():
    with pytest.raises(ValueError):
        validate_file_pathname(
            pathname="pachama/tests/test_data/text_files",
            is_file=True,
            allowed_extensions=["txt"],
        )


@pytest.mark.parametrize(
    "test_input,expected_error",
    [
        ("test_data/text_files/b a d name.txt", ValueError),  # contains space
        ("test_data/text_files/wrong_file_type.pdf", ValueError),  # wrong file type
        (f'test_data/text_files/rail/{"a"*512}.txt', ValueError),  # name too long
        ('test_data/text_files/z!@#$%^&*():;".txt', ValueError),  # invalid chars
    ],
)
def test_invalid_filename_raises_exception(test_input, expected_error):
    with pytest.raises(expected_error):
        validate_file_pathname(
            pathname=test_input, is_file=True, allowed_extensions=["txt"]
        )


def test_nonexistent_file_raises_exception():
    with pytest.raises(FileNotFoundError):
        validate_file_pathname(
            pathname="pachama/tests/test_data/test_data/text_files/i_dont_exist.txt",
            is_file=True,
            allowed_extensions=["txt"],
        )


def test_invalid_directory_raises_exception():
    with pytest.raises(FileNotFoundError):
        validate_file_pathname(
            pathname="pachama/tests/test_data/i_dont_exist/text_file.txt",
            is_file=True,
            allowed_extensions=["txt"],
        )


def test_absolute_path_raises_exception():
    with pytest.raises(ValueError):
        # Get absolute path
        FILE = Path(__file__).resolve()
        ROOT = FILE.parents[0]
        validate_file_pathname(
            pathname=str(ROOT / "test_data/text_files/test_text_file_0.txt"),
            is_file=True,
            allowed_extensions=["txt"],
        )
