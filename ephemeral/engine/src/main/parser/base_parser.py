"""
A library containing methods used for parsing jobs between python
data structures and json.
"""
import json


def parse_json_from_file(json_file):
    """Parses a json string and returns a python dictionary representing the json.
    """
    with open(json_file) as data_file:
        data = json.load(data_file)
    return data


def get_json_from_dict(py_dict):
    """Returns a json object string from a python dictionary.
    """
    return json.dumps(py_dict)
