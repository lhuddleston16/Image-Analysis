import re
import os
from pathlib import Path


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
