from typing import Any
from termcolor import colored
from enum import Enum
from py_wf.executor.executor import Executor
from py_wf.executor.python import PythonExecutor
from functools import wraps

class State(Enum):
    COMPLETED = 0
    FAILED = 1
    SUBMITTED = 2


class Task:

    def __init__(self, operator, executor: Executor,executor_flags={}):
        
        self.operator = operator
        self.executor = executor
        self.state = None

        self.executor_flags= executor_flags
        
    async def __call__(self,*args,**kwds):
        
        try:
            self.state = State.SUBMITTED
            self.output = await self.executor( self.operator(*args,**kwds) , **self.executor_flags )
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

def python_task(func):
    
    @wraps(func)
    def create_task():
        return Task(func,executor=PythonExecutor() )

    return create_task