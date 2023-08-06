import inspect
import sys
import time
from functools import lru_cache

from strategery.exceptions import TaskError, StrategyError
from strategery.logging import BypassLogger
from strategery.strategy import get_strategy
from strategery.tasks import Task, get_key

logger = None

def execute(*args, targets, input=None, preprocessed=None):
    resolved_logger = logger or BypassLogger()
    input = __renaming_preprocessed_to_input(preprocessed, input)
    if type(input) is list or type(input) is tuple:
        # Convert lists/tuples to type-indexed dictionary
        input = {type(p): p for p in input}

    queue = get_strategy(tuple(targets), preprocessed_keys=tuple(input.keys()))

    print('Processing strategy:', file=resolved_logger)
    for n, stage in enumerate(queue):
        print('Phase {}: {}'.format(n, [t.name() for t in stage]), file=resolved_logger)
    print("\n", file=resolved_logger)

    # Populate with preprocessed
    processed = input

    for stage in queue:
        for task in stage:
            if task not in processed:
                try:
                    ts = time.time()

                    __assert_task_type(task)

                    dependencies = __resolve_task_dependencies(task, processed)
                    processed[task] = task(*dependencies)

                    te = time.time()
                    print('[%2.2f sec] Processed: %r ' % (te - ts, task.name()),
                          file=resolved_logger)
                except Exception as e:
                    raise TaskError('Stategery failed at task {t}, found at approximately "{f}".\n\nInner error:\n{et}: {e}'.format(
                        t=task.name(),
                        et=type(e).__name__,
                        e=e,
                        f=task.code_file_colon_line(),
                    ))

    return tuple([processed[get_key(t)] for t in targets])


def __renaming_preprocessed_to_input(preprocessed, input):
    if preprocessed:
        __warn_once(
            'strategery warning: the argument `preprocessed` has been renamed to `input` '
            'and will be removed in a future version.',
        )
    if input and preprocessed:
        raise Exception('Cannot specify both `input` and `preprocessed')
    return input or preprocessed or {}


@lru_cache(1)
def __warn_once(message):
    print(message, file=sys.stderr)


def __assert_task_type(task):
    if not inspect.isfunction(task) and not inspect.isclass(task) and not hasattr(type(task), '__call__'):
        raise Exception("Task cannot be processed, '{t}' is not a function or a class.".format(t=task.name))


def __resolve_task_dependencies(task: Task, processed):
    if len(task.parameters) != len(task.dependencies):
        raise StrategyError('Stategery task {t} expects parameters {p}, @fed_by decorator only accounts for {d}'.format(
            t=task.name(),
            p=[k for k in task.signature.parameters.keys()],
            d=[d.name() for d in task.dependencies]
        ))

    values = []
    for parameter, dependency in zip(task.parameters.values(), task.dependencies):
        if dependency in processed:
            values.append(processed[dependency])
        elif parameter.default != inspect._empty:
            values.append(parameter.default)
        else:
            raise StrategyError('Strategery task {t} could not resolve parameter {p}.'.format(
                t=task.name(),
                p=parameter.name
            ))
    return values
