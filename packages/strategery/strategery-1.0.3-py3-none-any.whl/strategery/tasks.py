import inspect

from strategery.exceptions import TaskError
from strategery.features import StrategeryFeature


def get_key(obj):
    if isinstance(obj, str):
        return obj
    if hasattr(obj, "strategery_key"):
        return obj.strategery_key()
    return obj


class Task(object):
    def __init__(self, task):
        self.task = task
        self.compute = task
        self.dependencies = tuple()
        self.signature = tuple()
        self.parameters = {}
        self._key = get_key(task)

        if inspect.isclass(task) and issubclass(task, StrategeryFeature):
            if hasattr(task, 'compute'):
                self.compute = task.compute
            else:
                raise TaskError(
                    'Tasks inheriting the StrategeryFeature interface must implement @staticclass `builder`.\n' + \
                    'Task {t}, found at "{f}".'.format(
                    t=self.name(),
                    f=self.code_file_colon_line()
                ))

        if hasattr(self.compute, '_dependencies'):
            self.dependencies = self.compute._dependencies
            self.signature = inspect.signature(self.compute)
            self.parameters = self.signature.parameters


    def name(self):
        error_task = self._error_feedback_task()
        if isinstance(error_task, str):
            return "'{}'".format(error_task)
        module = ""
        if hasattr(error_task, '__module__'):
            module = '{}.'.format(error_task.__module__)
        if hasattr(error_task, '__qualname__'):
            return '{}{}'.format(module, error_task.__qualname__)
        if hasattr(error_task, '__name__'):
            return '{}{}'.format(module, error_task.__name__)
        try:
            return '{}{}'.format(module, type(error_task).__name__)
        except Exception:
            return '{}{}'.format(module, str(error_task))

    def code_first_line_number(self):
        error_task = self._error_feedback_task()
        try:
            if not self.callable():
                return None
            if hasattr(error_task, '__code__'):
                return error_task.__code__.co_firstlineno
            return '{}'.format(inspect.findsource(type(error_task))[1])
        except:
            return None

    def code_file_name(self):
        error_task = self._error_feedback_task()
        try:
            return inspect.getmodule(error_task).__file__
        except:
            return '(unknown file)'

    def code_file_colon_line(self):
        line_number = self.code_first_line_number()
        if not line_number:
            line_number = "0"
        return "{}:{}".format(self.code_file_name(), line_number)

    def _error_feedback_task(self):
        if self.compute == StrategeryFeature.compute:
            # This means a StrategeryFeature didn't implement `compute`
            return self.task
        return self.compute

    def callable(self):
        if inspect.isclass(self.compute):
            return False
        return callable(self.compute)

    def __call__(self, *args, **kwargs):
        return self.compute.__call__(*args, **kwargs)

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        return self._key == other

    def __str__(self):
        return 'Strategery Task: {}'.format(self.name())
