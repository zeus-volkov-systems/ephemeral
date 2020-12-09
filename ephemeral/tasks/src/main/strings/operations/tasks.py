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
    task_dict["capitalize_words"] = capitalize_closure
    task_dict["char_count"] = char_count_closure
    task_dict["combine_words"] = combine_words_closure
    return task_dict


def get_task(task_name, init_args):
    """
    Accesses the task dictionary, returning the task corresponding to a given key,
    wrapped in a closure containing the task and its arguments.
    """
    tasks = make_task_dict()
    return tasks[task_name](init_args)


def capitalize_closure(init_args):
    """
    A closure around the example function which is an endpoint in the task factory.
    """
    init_args = init_args
    async def capitalize_words(words_map):
        """
        A simple function to illustrate use of the task factory pattern.
        """
        words = words_map["strings"]
        capitalized_words = [word.upper() for word in words]
        return {"strings": capitalized_words}
    return capitalize_words


def char_count_closure(init_args):
    """
    A closure around the example function which is an endpoint in the task factory.
    """
    init_args = init_args
    async def char_count(words_map):
        """
        A simple function to illustrate use of the task factory pattern.
        """
        words = words_map["strings"]
        word_length = [len(word) for word in words]
        return {"lengths": word_length}
    return char_count


def combine_words_closure(init_args):
    """
    A closure around the example function which is an endpoint in the task factory.
    """
    combine_keys = init_args["dict_keys"]
    final_key = init_args["final_key"]
    async def combine_words(words_map):
        """
        A simple function to illustrate use of the task factory pattern.
        """
        return_dict = {final_key: ""}
        for combine_key in combine_keys:
            return_dict[final_key] += words_map[combine_key]
        return return_dict
    return combine_words
