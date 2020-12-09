"""
Library containing methods used for validating a datasource represented as a
python dictionary.
"""
import ephemeral.engine.src.main.validator.base_validator as base_validator


def validate_datasource(datasource):
    """Validates a datasource dictionary against its definition.
    """
    definition = get_datasource_definition()
    if validate_definition(datasource, definition):
        return True
    return False


def validate_field_definition(definition, actual):
    """Validates a given top level datasource key against its definition.
    Returns a boolean of the validation.
    """
    if base_validator.validate_type(actual, definition["type"]):
        return True
    return False


def validate_definition(datasource, definition):
    """Validates the datasource against the given definition.
    """
    valid_list = [validate_field_definition(defn, datasource[defn["name"]])
                  for defn in definition["fields"]]
    valid = list(set(valid_list))
    if len(valid) == 1 and valid[0]:
        return True
    return False


def get_datasource_definition():
    """Returns the formal definition for a datasource as a python dictionary.
    """
    return base_validator.get_main_definition("datasource")
