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
    task_dict["example"] = example_closure
    return task_dict

def get_task(task_name, init_args):
    """
    Accesses the task dictionary, returning the task corresponding to a given key,
    wrapped in a closure containing the task and its arguments.
    """
    tasks = make_task_dict()
    return tasks[task_name](init_args)

def example_closure(init_args):
    """
    A closure around the example function which is an endpoint in the task factory.
    """
    test_arg = init_args["example_property"]
    async def example(data, example_property=test_arg):
        """
        A simple function to illustrate use of the task factory pattern.
        """
        print("executing the task.")
        print("Input data submitted: ", data["input"])
        print(example_property, " equals ", test_arg)
        x = {"input": "We got: " + test_arg + data["input"]}
        return x
    return example
