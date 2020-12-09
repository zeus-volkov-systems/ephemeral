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
    task_dict["split_list"] = split_list_closure
    return task_dict

def get_task(task_name, init_args):
    """
    Accesses the task dictionary, returning the task corresponding to a given key,
    wrapped in a closure containing the task and its arguments.
    """
    tasks = make_task_dict()
    return tasks[task_name](init_args)

def split_list_closure(init_args):
    """
    A closure around the split_string function which is an endpoint in the task factory.
    """
    list_to_split = init_args["list_key"]
    key_to_add = init_args["key_name"]
    async def split_list(list_map):
        """
        Splits a string into a list and returns it.
        """
        return_list = []
        for list_item in list_map[list_to_split]:
            return_dict = {}
            return_dict[key_to_add] = list_item
            for dict_key in list_map:
                if dict_key != list_to_split:
                    return_dict[dict_key] = list_map[dict_key]
            return_list.append(return_dict)
        return return_list
    return split_list
