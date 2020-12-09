"""
The file_utils module provides methods for accessing or manipulating the
filesystem.
"""

from ephemeral.definitions import ROOT_DIR


def get_relative_package_path():
    """Gets the relative path for the package useful to finding package relative
    property files or other resources.
    """
    return ROOT_DIR
