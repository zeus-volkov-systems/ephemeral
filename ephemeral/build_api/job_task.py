import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ephemeral.build_api import LibFunction


logger = logging.getLogger(__name__)


class JobTask(object):
    def __init__(self, name: str, type: str, lib_function: 'LibFunction', parent: 'JobTask'):
        self.name = name
        self.type = type
        self.lib_function = lib_function
        self.parent = parent
        self.consumes = None
        self.produces = None
        self.init_args = {}
        self._task_created_callback = None

    def new_task_created(self, new_task):
        if self._task_created_callback:
            return self._task_created_callback(new_task)
        else:
            raise RuntimeError('No _task_created_callback has been set!')

    def set_task_created_callback(self, cb):
        self._task_created_callback = cb

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'method': self.lib_function.method_str,
            'namespace': self.lib_function.namespace,
            'consumes': '---',
            'produces': '----',
            'init_args': self.init_args
        }








