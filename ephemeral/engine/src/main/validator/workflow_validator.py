"""
Library containing methods used for validating a datasource represented as a
python dictionary.
"""


def validate_workflow(workflow, tasks):
    """Validates a workflow using tasks.
    """
    valid_list = [validate_workflow_element(element, tasks) for element in workflow]
    valid = list(set(valid_list))
    if len(valid) == 1 and valid[0]:
        return True
    return False


def validate_workflow_element(element, tasks):
    """Validates a single workflow element using task consumption and production
    matching.
    """
    if len(element) is not 2:
        return False
    input_task = get_matching_task(element[0], tasks)
    output_task = get_matching_task(element[1], tasks)
    if input_task["type"] == "function" and output_task["type"] == "function":
        if input_task["produces"] == output_task["consumes"]:
            return True
        return False
    else:
        return True


def get_matching_task(task_name, tasks):
    """Returns a task if it matches the given name.
    """
    for task in tasks:
        if task["name"] == task_name:
            return task
    return None
