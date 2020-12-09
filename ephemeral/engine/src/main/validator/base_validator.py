"""
The base module for validators containing generic and/or common methods
useful to other validators.
"""

import json
import ephemeral.engine.src.main.utils.file_utils as file_utils
import ephemeral.engine.src.main.utils.math_utils as math_utils


MAIN_DEFINITION_PATH = "/engine/resources/main/definitions/"

FILE_DICT = {
    "job": "job.json",
    "datasource": "datasource.json",
    "task": "task.json"
}

TYPE_DICT = {
    "map": dict,
    "string": str,
    "list": list,
    "integer": int
}


def is_valid(test_list):
    """Tests whether a list of booleans is valid (all True)
    """
    test = list(set(test_list))
    if len(test) == 1 and test[0]:
        return True
    return False


def get_main_definition(def_type):
    """Returns a definition from the filesystem based on a type.
    """
    file_name = FILE_DICT[def_type]
    package_path = file_utils.get_relative_package_path()
    file_path = package_path + MAIN_DEFINITION_PATH + file_name
    with open(file_path) as data_file:
        data = json.load(data_file)
    return data


def get_unique_id(length=10):
    """Returns a unique string id for the given length.
    """
    return math_utils.get_random_string(length)


def validate_type(test_object, object_type):
    """Validates the type of an object against the passed type.
    """
    if TYPE_DICT[object_type] == type(test_object):
        return True
    return False
