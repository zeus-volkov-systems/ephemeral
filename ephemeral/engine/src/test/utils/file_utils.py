"""
The file_utils module provides methods for accessing or manipulating the
filesystem.
"""

from ephemeral.definitions import ROOT_DIR


def replace_path_keyword(path, keyword='{}'):
    """Replaces the given keyword with the relative (root) path.
    """
    return path.replace(keyword, ROOT_DIR)
