import functools

from strategery.tasks import Task


def fed_by(*args, **kwargs):
    """This is a decorator to indicate you'd like your Feature task to get other Feature tasks injected into it"""
    def wrapper(function):
        @functools.wraps(function)
        def decorator():
            function._dependencies = [Task(dep) for dep in args]
            return function
        return decorator()
    return wrapper
