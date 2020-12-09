"""
Contains business logic tasks for this order of the task factory.
Each task should be wrapped inside a task closure that accepts a dictionary parameter
used for task initialization.
"""

import ephemeral.library.src.test.xarray.dataset as dataset
import ephemeral.library.src.test.dask.executor as executor


def make_task_dict():
    """
    Returns a task dictionary containing all tasks in this module.
    """
    task_dict = {}
    task_dict["get_statistic"] = get_statistic_closure
    return task_dict

def get_task(task_name, init_args):
    """
    Accesses the task dictionary, returning the task corresponding to a given key,
    wrapped in a closure containing the task and its arguments.
    """
    tasks = make_task_dict()
    return tasks[task_name](init_args)

def get_statistic_closure(init_args):
    """
    A closure around the load dataset function. Returns a dataset.
    """
    statistic = init_args["statistic"]
    async def get_statistic(data, statistic=statistic):
        """
        Returns the specified statistic as a future (runs on dask distributed).
        """
        print("Getting the stat function for a statistic: ", statistic)
        stat_function = dataset.get_statistic_function(statistic)
        future = executor.run_one(data["client"], stat_function, data["dataset"])
        print("Got a future for the statistic: ", future)
        return {"future": future}
    return get_statistic
