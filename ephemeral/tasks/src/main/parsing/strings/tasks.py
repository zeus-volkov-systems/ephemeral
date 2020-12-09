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
    task_dict["split_string"] = split_string_closure
    task_dict["filter_string_length"] = filter_strings_closure
    return task_dict

def get_task(task_name, init_args):
    """
    Accesses the task dictionary, returning the task corresponding to a given key,
    wrapped in a closure containing the task and its arguments.
    """
    tasks = make_task_dict()
    return tasks[task_name](init_args)

def split_string_closure(init_args):
    """
    A closure around the split_string function which is an endpoint in the task factory.
    """
    init_args = init_args
    async def split_string(string_map):
        """
        Splits a string into a list and returns it.
        """
        input_string = string_map["input"]
        split_string = input_string.split()
        return {"strings": split_string}
    return split_string

def filter_strings_closure(init_args):
    """
    A closure around the split_string function which is an endpoint in the task factory.
    """
    word_length = init_args["word_length"]
    comparison = init_args["comparison"]

    async def filter_string_length(strings_map, word_length=word_length, comparison=comparison):
        """
        Splits a string into a list and returns it.
        """
        string_list = strings_map["strings"]
        if comparison == "less":
            filtered_strings = [string for string in string_list if len(string) < word_length]
        elif comparison == "greater":
            filtered_strings =  [string for string in string_list if len(string) > word_length]
        else:
            filtered_strings = string_list
        return {"strings": filtered_strings}
    return filter_string_length
