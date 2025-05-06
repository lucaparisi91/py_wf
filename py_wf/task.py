from termcolor import colored
from enum import Enum
from py_wf.executor.executor import Executor


class State(Enum):
    COMPLETED = 0
    FAILED = 1
    SUBMITTED = 2


class Task:

    def __init__(self, *args, executor: Executor, **kwds):
        self.args = args
        self.kwds = kwds
        self.executor = executor
        self.executor = executor
        self.state = None

    async def __call__(self):

        try:
            self.state = State.SUBMITTED
            self.output = await self.executor(*self.args, **self.kwds)
        except Exception as e:
            print(colored(f"Error in submitting jobs: {str(e)} ", "red"))
            self.state = State.FAILED
        else:
            self.state = State.COMPLETED

        return self

    def __repr__(self) -> str:
        return f"""<Task operator={repr(self.operator)}
                    executor={ repr(self.executor)},
                    resources={repr(self.resources)}>
                """
