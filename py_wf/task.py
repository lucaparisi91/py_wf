from pathlib import Path
import os
from termcolor import colored
from enum import Enum

class State(Enum):
        COMPLETED = 0
        FAILED = 1
        DEPENDENCIES = 2


class Task:
    
    def __init__(self,operator,executor,resources={},work_dir: str = "."):
        self.operator=operator
        self.executor=executor
        self.resources=resources
        self.executor=executor
        self.work_dir=work_dir
        self.state=None
        self.output=None
        

    async def __call__(self):
        
        try:
            self.output = await self.executor(self.operator)
        except Exception as e:
            print( colored( f"Error in submitting jobs: {str(e)} ","red") )
            self.state=State.FAILED
        else:
            self.state=State.COMPLETED
        
        return self
        
        #except Exception as e:
        #    
            
        #print(f"Task {self.name} completed with state " , colored( self.executor.get_state(jobid) , "yellow" ) )

    def __repr__(self) -> str:
        return f"<operator={repr(self.operator)} executor={ repr(self.executor)},resources={repr(self.resources)}>"