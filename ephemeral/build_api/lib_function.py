import logging
from ephemeral.build_api import type_util
from ephemeral.build_api.job_task import JobTask

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass #from ephemeral.engine.src.main.build_api.job_task import JobTask

logger = logging.getLogger(__name__)


class LibFunction(object):
    def __init__(self, name: str, method_ref, consumes=None, produces=None):
        self.name = name
        self.method_ref = method_ref
        self.namespace = 'main.example'
        self.method_str = method_ref.__name__

        # Set the consumes and produces properties, always using the consumes and produces arguments
        # when they are provided. If are not provided, try to infer them from type annotations
        # When the argument is not provided and the types cannot be inferred, give a warning.
        warn_str = ("The '{}' argument was not supplied and could not be inferred by type annotations. "
                    "Any tasks using this function will have to supply this argument.")

        self.consumes = consumes or type_util.infer_function_param_types(method_ref)
        if not self.consumes:
            logger.warning(warn_str.format('consumes'))

        self.produces = produces or type_util.infer_function_return_type(method_ref)
        if not self.produces:
            logger.warning(warn_str.format('produces'))

    def __call__(self, task: 'JobTask', task_name: str, **lib_func_args):
        """
        When a lib function is called,
        :param task:
        :param task_name:
        :param lib_func_args:
        :return:
        """
        # TODO: Parse out input tasks from function args: In the future aggregation functions may be introduced, so
        # lib functions could accept more than one task at a time. For now, assume all **kwargs (lib_func_args) are
        # arguments intended for the library function

        # TODO Validate types


        init_args = lib_func_args

        # Create new task created by using this function
        task_result = JobTask(
                name=task_name,
                type='function',
                lib_function=self,
                parent=task
            )
        task_result.init_args = init_args
        return task.new_task_created(task_result)


