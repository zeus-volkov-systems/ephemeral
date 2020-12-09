"""
Used to drive the building and processing of tasks.
"""

import ephemeral.tasks.src.main.task_factory as task_factory

def build_tasks(job_map):
    """Uses a valid job map to build a list of tasks.
    """
    tasks = job_map["tasks"]
    final_tasks = [build_task(task, job_map["workflow"], tasks) for task in tasks]
    final_tasks = [task for task in final_tasks if task]
    return final_tasks

def build_route_list(namespace):
    """Builds a routing list for use by the task factory.
    """
    return namespace.split(".")

def build_task(task, workflow, tasks):
    """Builds a task using the task definition and the task_factory.
    """
    if task["type"] == "function":
        task_function = (task_factory.get_task(build_route_list(task["namespace"]),
                                               task["method"], task["init_args"]))
        parent = get_parent_task(task, workflow, tasks)
        return build_function_task(task, task_function, parent)
    elif task["type"] == "input":
        return build_input_task(task)
    elif task["type"] == "output":
        parent = get_parent_task(task, workflow, tasks)
        return build_output_task(task, parent)

def get_parent_task(task, workflow, tasks):
    """
    Returns the name of the task which the target task is dependent on, as
    specified in the workflow. All tasks can have only one direct parent task.
    """
    for element in workflow:
        if element[1] == task["name"]:
            return get_task_id(element[0], tasks)
    return None

def get_task_id(task_name, tasks):
    """Returns the unique id for the given task.
    """
    for task in tasks:
        if task["name"] == task_name:
            return task["id"]

def build_function_task(task, function, parent):
    """Builds a task dictionary using a task and a function.
    """
    task_dictionary = {}
    task_dictionary["id"] = task["id"]
    task_dictionary["name"] = task["name"]
    task_dictionary["type"] = "function"
    task_dictionary["method"] = function
    task_dictionary["parent"] = parent
    return task_dictionary

def build_input_task(task):
    """Builds a task dictionary for an input task type.
    """
    task_dictionary = {}
    task_dictionary["id"] = task["id"]
    task_dictionary["type"] = "input"
    task_dictionary["name"] = task["name"]
    task_dictionary["method"] = get_input_function()
    task_dictionary["parent"] = None
    return task_dictionary

def build_output_task(task, parent):
    """Builds a task dictionary for an output task type.
    """
    task_dictionary = {}
    task_dictionary["id"] = task["id"]
    task_dictionary["type"] = "output"
    task_dictionary["name"] = task["name"]
    task_dictionary["data"] = []
    task_dictionary["method"] = get_output_function()
    task_dictionary["parent"] = parent
    return task_dictionary

def get_output_function():
    """Returns a function that will get called when the output function
    is run in the job map.
    """
    async def output_function(task, data):
        """There are an arbitrary number of output functions on a job map.
        Therefore, each must hold its own data.
        """
        task["data"].append(data)
    return output_function

def get_input_function():
    """Returns a function that will get called when the input function
    is run in the job map.
    """
    async def input_function(data):
        """Currently job maps only support one datasource and one input task.
        With only one input function, it only needs to pass through its data.
        """
        return data
    return input_function

def get_output_tasks(tasks):
    """Returns all output tasks in a list.
    """
    return [task for task in tasks if task["type"] == "output"]

def build_task_map(tasks):
    """Creates a task map used for task execution. The map should be a dict
    of dicts - the top level dict should hold a key for each task. The
    """
    return {"task_"+task["id"]:get_task_map_value(task) for task in tasks}

def get_task_map_value(task):
    """Returns the appropriate body for a task on a task map based on type.
    Input tasks automatically get a todo value of 1, other tasks get a todo
    value of 0.
    """
    if task["type"] == "input":
        return {"todo": 1, "complete": 0}
    else:
        return {"todo": 0, "complete": 0}
