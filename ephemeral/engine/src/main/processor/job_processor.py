"""This module handles control of job execution.
"""

import asyncio

import ephemeral.engine.src.main.processor.task_processor as task_processor


def run_job(tasks, task_map, data):
    """Asynchronously executes a job workflow. Takes a list of tasks, a map of
    dicts for each task that determines how many times each must run, and a dict of
    input data. Does not return a value, but completes and returns when the job
    has finished (when each task has executed for each of its inputs or an error
    has occurred.)
    """
    loop = asyncio.get_event_loop()
    for task in tasks:
        if task["parent"] is None:
            task_processor.run_task(loop, task, data, tasks, task_map)
    loop.run_forever()
