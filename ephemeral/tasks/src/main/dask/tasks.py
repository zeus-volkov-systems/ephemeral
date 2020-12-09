"""
Contains business logic tasks for this order of the task factory.
Each task should be wrapped inside a task closure that accepts a **kargs parameter
used for task initialization.
"""

import ephemeral.library.src.test.dask.connection as connection
import ephemeral.library.src.test.dask.executor as executor
import ephemeral.library.src.test.xarray.dataset as dataset

def make_task_dict():
    """
    Returns a task dictionary containing all tasks in this module.
    """
    task_dict = {}
    task_dict["dask_connect"] = dask_connect_closure
    task_dict["get_result"] = get_result_closure
    return task_dict

def get_task(task_name, init_args):
    """
    Accesses the task dictionary, returning the task corresponding to a given key,
    wrapped in a closure containing the task and its arguments.
    """
    tasks = make_task_dict()
    return tasks[task_name](init_args)

def dask_connect_closure(init_args):
    """
    A closure around the example function which is an endpoint in the task factory.
    """
    init_args = init_args
    async def dask_connect(data):
        """
        Creates a local connection client and adds it to the task map.
        """
        print("executing the dask test task.")
        dask_connection = connection.create_local_environment()
        print("Setup a local test dask client.")
        data["client"] = dask_connection
        return data
    return dask_connect

def get_result_closure(init_args):
    """
    A closure around the example function which is an endpoint in the task factory.
    """
    init_args = init_args
    async def get_result(data):
        """
        Grabs the result from a future. Blocks until the result is returned.
        Definitely do not use unless you are testing or it is a small dataset.
        """
        print("Coercing a local result from our dask future.")
        data_set = executor.get_result(data["future"])
        value = dataset.get_as_list(data_set)
        print("Returning from getting a result.")
        return {"value":value}
    return get_result
