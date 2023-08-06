import inspect
from functools import lru_cache
from typing import List

from strategery.exceptions import StrategyError
from strategery.tasks import Task


def get_requirements(targets, preprocessed) -> List[Task]:
    requirements = set([Task(t) for t in targets if Task(t) not in preprocessed])
    visited = set([Task(key) for key in preprocessed])

    while True:
        to_visit = [req for req in requirements if req not in visited]
        if len(to_visit) is 0:
            break
        for task in to_visit:
            visited.add(task)
            if len(task.dependencies):
                parameters = task.signature.parameters.values()
                for parameter, dep in zip(parameters, task.dependencies):
                    if not dep.callable() and dep not in preprocessed:
                        if parameter.default != inspect._empty:
                            continue
                        else:
                            raise StrategyError('Task {t} failed, expected parameter {d}, but parameter was not found.\nat "{f}".'.format(
                                t=task.name(),
                                d=dep.name(),
                                f=task.code_file_colon_line()
                            ))
                    if dep not in visited:
                        requirements.add(dep)

    return requirements


def dependencies_met(task, queue, preprocessed):
    flat = set(preprocessed)
    for stage in queue:
        flat = flat.union(stage)

    if len(task.dependencies):
        parameters = task.signature.parameters.values()
        for parameter, dep in zip(parameters, task.dependencies):
            if dep not in flat and parameter.default == inspect._empty:
                return False

    return True


@lru_cache()
def get_strategy(targets, preprocessed_keys):
    requirements = get_requirements(targets, preprocessed_keys)
    queue = []
    while len(requirements) > 0:
        ready_tasks = [req for req in requirements if dependencies_met(req, queue, preprocessed_keys)]
        if len(ready_tasks) > 0:
            queue.append(ready_tasks)
            for task in ready_tasks:
                requirements.remove(task)
            continue

        raise Exception("Couldn't resolve a strategy for targets {} ".format(targets))
    return queue