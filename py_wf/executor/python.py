from py_wf.executor.executor import Executor
from py_wf.task import Task
import asyncio
from functools import wraps


class PythonExecutor(Executor):
    """Python executor for python functions

    Inteded to be a light wrapper to present an async
    interface to a synchroneous python function.
    """

    def __init__(self):
        pass

    def __call__(self, func, *args, **kwds) -> asyncio.Task:
        async def run_python_func(func, *args, **kwds):

            return func(*args, **kwds)

        return asyncio.create_task(run_python_func(func, *args, **kwds))


def python_task(func):

    @wraps(func)
    def create_task():
        return Task(func, executor=PythonExecutor())

    return create_task
