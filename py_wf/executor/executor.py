from typing import Any
from subprocess import check_output, STDOUT
import asyncio 
from abc import ABC,abstractmethod


class Executor(ABC):
    """ Abstract base class for all executors

    An executor is a callable. When invoked, possibly with parameters, it is responsponsible to create an asynchroneous tasks that takes cares to submit to a scheduler ( i.e. slurm, current python session, bash etc..) and returns once the task is completed.
    """
    
    @abstractmethod
    def __call__(self, *args,**kwds) -> asyncio.Task:
        """Create an asynchroneous task to be run with asyncio.
        """
        pass


