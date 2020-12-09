"""
Retrieves a task method for the given input routing parameters.
"""
import ephemeral.tasks.src.main.tasks as tasks
from ephemeral.tasks.src.main.parsing.task_factory import (
    get_task as get_parsing_task)
from ephemeral.tasks.src.main.strings.task_factory import (
    get_task as get_string_task)
from ephemeral.tasks.src.main.dask.task_factory import (
    get_task as get_dask_task)
from ephemeral.tasks.src.main.xarray.task_factory import (
    get_task as get_xarray_task)


def make_task_dict():
    """Defines the routing for this task order.
    """
    task_dict = {}
    task_dict["parsing"] = get_parsing_task
    task_dict["strings"] = get_string_task
    task_dict["dask"] = get_dask_task
    task_dict["xarray"] = get_xarray_task
    return task_dict

def route(key, task_method, route_list, init_args):
    """Retrieves the proper route for the given parameter.
    """
    task_dict = make_task_dict()
    return task_dict[key](route_list, task_method, init_args)

def get_task(route_list, task_method, init_args=None):
    """
    Retrieves the task for the given string.
    Routing should be a list of string arguments that determine where to go.
    If passed, init_args should be a python dictionary
    holding key-value pairs to be used in endpoint function initialization.
    """
    route_list.pop(0)
    if route_list:
        return route(route_list[0], task_method, route_list, init_args)
    else:
        return tasks.get_task(task_method, init_args)
