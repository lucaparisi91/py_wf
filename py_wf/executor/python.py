from py_wf.executor.executor import Executor
import asyncio


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
