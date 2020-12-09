"""This module handles execution of job tasks.
"""
import logging
from functools import partial as build_func

logger = logging.getLogger(__name__)
def task_callback(loop, task, tasks, task_map, future):
    """Gets called when a task has finished executing.
    Determines whether the result produced by the task is a map or a
    list of maps, updates the completed count for the task, checks to see
    if all tasks have been executed for all inputs, and runs all children
    tasks with all input data sets.
    """

    try:
        data = future.result()
    except:
        # There should be a better way to handle this. For now, log the exception and stop event loop
        logger.exception('Exception thrown while getting task result.', exc_info=True)
        loop.stop()
        return

    data_type = get_data_type(data)
    if not data_type and task["type"] != "output":
        logger.error("Invalid data type returned from task.")
        loop.stop()
    else:
        update_task_complete_count(task_map, task)
        if check_job_complete(task_map):
            loop.stop()
        else:
            for child_task in tasks:
                if child_task["parent"] == task["id"]:
                    update_task_todo_count(task_map, child_task, data)
                    if data_type == "dict":
                        run_task(loop, child_task, data, tasks, task_map)
                    elif data_type == "list":
                        for data_member in data:
                            run_task(loop, child_task, data_member, tasks, task_map)


def run_task(loop, task, data, tasks, task_map):
    """Used to run a given task.
    """
    logger.info('Running task name: "%s"', task.get('name'))
    if task["type"] == "output":
        task_future = loop.create_task(task["method"](task, data))
    else:
        task_future = loop.create_task(task["method"](data))
    task_future.add_done_callback(build_func(task_callback, loop, task, tasks, task_map))


def get_data_type(data):
    """Qualifies and returns the type of data as a string. If not an acceptable
    type, returns None.
    """
    if type(data) is dict:
        return "dict"
    elif type(data) is list:
        return "list"
    else:
        return None


def check_job_complete(task_map):
    """Validates a map for every task id. Ensures that each task has been
    run the required number of times.
    """
    valid_list = [check_task_complete(task_map[task]) for task in task_map]
    valid = list(set(valid_list))
    if len(valid) == 1 and valid[0]:
        return True
    return False


def check_task_complete(task):
    """Validates a single task for its todo value against its complete value.
    """
    if task["todo"] and task["todo"] == task["complete"]:
        return True
    return False


def update_task_todo_count(task_map, task, data):
    """Updates the count of a task's todo value on a task map.
    Sets the number of times a task must be executed to be considered
    complete.
    """
    data_type = get_data_type(data)
    if data_type == "dict":
        task_map["task_"+task["id"]]["todo"] += 1
    elif data_type == "list":
        task_map["task_"+task["id"]]["todo"] += len(data)
    return


def update_task_complete_count(task_map, task):
    """Updates the completed count for a given task on the task map.
    """
    task_map["task_"+task["id"]]["complete"] += 1
    return
