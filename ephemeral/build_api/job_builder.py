from ephemeral.engine.src.main.driver.task_driver import get_input_function
from ephemeral.build_api.lib_function import LibFunction
from ephemeral.build_api.job_task import JobTask


class JobBuilder(object):

    def __init__(self, job_name):
        self.job_name = job_name
        self.input_task = None
        self.input_data = None
        self._tasks = []

    def _add_task(self, task: JobTask):
        self._tasks.append(task)

    def create_input_task(self, data, name='in') -> JobTask:
        if self.input_data:
            raise ValueError('Input task has already been created!')

        self.input_data = data
        input_function = LibFunction('input', get_input_function())
        input_task = JobTask(name=name, type='input', lib_function=input_function, parent=None)
        input_task.set_task_created_callback(self._task_created)
        self.input_task = input_task
        self._add_task(input_task)
        return input_task

    def _task_created(self, task: JobTask):
        """
        Called when a task is created for this job.
        Validate, add to job tasks, and return the task if valid
        :param task:
        :return: the task if valid
        """
        # TODO: Make sure the task is valid. check to make sure task name is unique in this job context
        # TODO: Map input keys from previous task to this task

        # Set the callback to be called when a new task is created from this task
        task.set_task_created_callback(self._task_created)
        self._add_task(task) # Add to task collection
        return task

    def print_tasks(self):
        for t in self._tasks:
            print(t.to_dict())