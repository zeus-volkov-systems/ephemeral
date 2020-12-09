"""
Library containing methods used for validating tasks represented as a python
dictionaries.
"""
import ephemeral.engine.src.main.parser.base_parser as base_parser
import ephemeral.engine.src.main.validator.base_validator as base_validator
import ephemeral.engine.src.main.utils.file_utils as file_utils

VALUE_DEFINITION_PATH = "/tasks/resources/main/tasks/"


def validate_tasks(tasks):
    """Validates a list of given tasks against both the general task definition
    and the individual task value definition.
    """
    definition = get_task_definition()
    functions = [validate_task(task, definition) for task in tasks if
                 is_function_task(task)]
    inputs = [validate_input(task) for task in tasks if is_input_task(task)]
    outputs = [validate_output(task) for task in tasks if is_output_task(task)]
    if (base_validator.is_valid(functions) and base_validator.is_valid(inputs)
            and base_validator.is_valid(outputs)):
        return True
    return False


def is_function_task(task):
    """Used to filter if the task is a function task.
    """
    if task["type"] == "function":
        return True
    return False


def is_input_task(task):
    """Used to filter if the task is an input task.
    """
    if task["type"] == "input":
        return True
    return False


def is_output_task(task):
    """Used to filter if the task is an output task.
    """
    if task["type"] == "output":
        return True
    return False


def validate_task(task, definition):
    """Validates a single task against both the general task definition and
    the individual task value definition.
    """
    value_definition = get_value_definition(task)
    if 'id' not in task:
        task['id'] = get_unique_task_id()
    if validate_definition(task, definition) and validate_value(task, value_definition):
        return True
    return False


def validate_input(task):
    """Validates a single input task. Adds an id if none exists.
    """
    if 'id' not in task:
        task['id'] = get_unique_task_id()
    return True


def validate_output(task):
    """Validates a single output task. Adds an id if none exists.
    """
    if 'id' not in task:
        task['id'] = get_unique_task_id()
    return True


def validate_definition(task, definition):
    """Validates the task against the given definition.
    """
    valid_list = [validate_field_definition(defn, task[defn["name"]])
                  for defn in definition["fields"]]
    valid = list(set(valid_list))
    if len(valid) == 1 and valid[0]:
        return True
    return False


def validate_value(task, definition):
    """Validates a task against its task specific definition.
    """
    if (validate_consumption(task, definition)
            and validate_production(task, definition)
            and validate_init_args(task, definition)):
        return True
    return False


def validate_init_args(task, definition):
    """Validates initial args for a given task against its definition.
    """
    if not task["init_args"] and not definition["init_args"]:
        return True
    valid_list = [validate_init_arg(key, task["init_args"][key],
                                    definition["init_args"]) for key in
                  task["init_args"]]
    valid = list(set(valid_list))
    if len(valid) == 1 and valid[0]:
        required_args = [arg["name"] for arg in definition["init_args"] if arg["required"]]
        present_args = list(task["init_args"].keys())
        missing_required = set(required_args) - set(present_args)
        if not missing_required:
            return True
    return False


def validate_init_arg(arg_name, arg_value, arg_definitions):
    """Validates an initial argument in a task against its definition.
    """
    arg_definition_names = [arg["name"] for arg in arg_definitions]
    if arg_name not in arg_definition_names:
        return False
    for arg_def in arg_definitions:
        if arg_def["name"] == arg_name:
            if base_validator.validate_type(arg_value, arg_def["type"]):
                return True
            return False
    return False


def validate_consumption(task, definition):
    """Validates the type of task consumption.
    """
    if task["consumes"] in definition["consumes"]:
        return True
    return False


def validate_production(task, definition):
    """Validates the type of task consumption.
    """
    if task["produces"] in definition["produces"]:
        return True
    return False


def validate_field_definition(definition, actual):
    """Validates a given top level job key against its definition.
    Returns a boolean of the validation.
    """
    if base_validator.validate_type(actual, definition["type"]):
        return True
    return False


def get_task_definition():
    """Returns the formal definition for a task as a python dictionary.
    """
    return base_validator.get_main_definition("task")


def get_unique_task_id():
    """Returns a unique job id for the job.
    """
    return base_validator.get_unique_id(15)


def get_value_definition(task):
    """Returns a definition from the filesystem based on a task name.
    """
    namespace_path = task["namespace"].replace(".", "/") + "/"
    file_name = task["method"] + ".json"
    package_path = file_utils.get_relative_package_path()
    file_path = package_path + VALUE_DEFINITION_PATH + namespace_path + file_name
    return base_parser.parse_json_from_file(file_path)
