
from pathlib import Path
import os
import subprocess
import time
import sys
from termcolor import colored
import logging

logger = logging.getLogger(__name__)


class task:
    
    def __init__(self,name:str,script:str,executor,resources={},work_dir: str = "."):
        self.name=name
        self.script=script
        self.resources=resources
        self.executor=executor
        self.work_dir=work_dir
        
    def __call__(self):

        jobid=self.executor.submit(task=self,work_dir=self.work_dir)
        
        self.executor.wait(jobid)

        try:
            self.executor.wait(jobid)
        except Exception as e:
            print( colored( f"Error in submitting jobs: {str(e)} ","red") )
        else:
            print(f"Task {self.name} completed with state " , colored( self.executor.get_state(jobid) , "yellow" ) )

    def __repr__(self) -> str:
        return f"<name={repr(self.name)},script={ repr(self.script)},resources={repr(self.resources)}>"
    