"""
Contains business logic tasks for this order of the task factory.
Each task should be wrapped inside a task closure that accepts a **kargs parameter
used for task initialization.
"""

def make_task_dict():
    """
    Returns a task dictionary containing all tasks in this module.
    """
    task_dict = {}
    return task_dict

def get_task(task_name, params):
    """
    Accesses the task dictionary, returning the task corresponding to a given key,
    wrapped in a closure containing the task and its arguments.
    """
    tasks = make_task_dict()
    return tasks[task_name](params)
