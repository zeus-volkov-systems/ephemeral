"""
Contains business logic tasks for this order of the task factory.
Each task should be wrapped inside a task closure that accepts a dictionary parameter
used for task initialization.
"""

import ephemeral.engine.src.test.utils.file_utils as file_utils
import ephemeral.library.src.test.xarray.dataframe as dataframe
import ephemeral.library.src.test.xarray.dataset as dataset
import ephemeral.library.src.test.dask.executor as executor


def make_task_dict():
    """
    Returns a task dictionary containing all tasks in this module.
    """
    task_dict = {}
    task_dict["load_dataframe"] = load_dataframe_closure
    task_dict["load_dataset"] = load_dataset_closure
    return task_dict

def get_task(task_name, init_args):
    """
    Accesses the task dictionary, returning the task corresponding to a given key,
    wrapped in a closure containing the task and its arguments.
    """
    tasks = make_task_dict()
    return tasks[task_name](init_args)

def load_dataframe_closure(init_args):
    """
    A closure around the load dataframe function. Returns a dataset.
    """
    chunk_size = init_args["chunk_size"]
    chunk_parameter = init_args["chunk_parameter"]
    async def load_dataframe(data, chunk_parameter=chunk_parameter, chunk_size=chunk_size):
        """
        Loads a dataframe from the netcdf resource in the task map. Uses
        the specified chunk parameter and chunk size.
        """
        print("Running load dataframe task.")
        file_name = file_utils.replace_path_keyword(data["path"])
        print(file_name)
        data_frame = dataframe.make_from_netcdf(file_name)#, chunk_parameter, chunk_size)
        data["dataframe"] = data_frame
        print("Got the dataframe.", data_frame)
        return data
    return load_dataframe

def load_dataset_closure(init_args):
    """
    A closure around the load dataset function. Returns a dataset.
    """
    variable = init_args["variable"]
    async def load_dataset(data, variable=variable):
        """
        Loads a dataset from the given variable existing in the given dataframe.
        Adds the dataset to the task map and returns the task map.
        """
        print("Loading a dataset from a data frame.")
        data_set = dataset.make_on_variable(data["dataframe"], variable)
        data["dataset"] = data_set
        print("Loaded the dataset.", data_set)
        return data
    return load_dataset
