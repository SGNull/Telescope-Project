"""
Tools for manipulating files paths.

Contains common helpful functions not present in OS.Path like:
    - get_file_name - Returns just the file name without extensions.
    - remove_file_extension - Returns the path without extensions.
"""


def remove_file_extension(file_path: str) -> str:
    """Returns the file path without any file extensions."""
    file_path_parts = file_path.split('\\')
    file = file_path_parts[-1]
    file_name = file.split('.')[0]
    return '\\'.join(file_path_parts[:-1] + [file_name])


def get_file_name(file_path: str) -> str:
    """Returns only the name of the given file."""
    file = file_path.split('\\')[-1]
    return file.split('.')[0]
