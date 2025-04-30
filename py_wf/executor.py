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


class PythonExecutor(Executor):
    """ Python exector for python functions
    
    Inteded to be a light wrapper to present an async interface to a synchroneous python function.
    """

    def __init__(self):
        pass
    
    def __call__(self,func,*args,**kwds) -> asyncio.Task:
            async def run_python_func(func,*args,**kwds):

                return func(*args,**kwds)
            
            return asyncio.create_task( run_python_func(func,*args,**kwds) )

class ShellExecutor(Executor):

    def __init__(self,preScript: str = "", maxProcesses : int = 4) :
        self.preScript=preScript
        self.maxProcesses=maxProcesses
        self._nProcess=0
        self.pollingTime=1
    
    def __call__(self, script: str) -> asyncio.Task :
        full_script= self.preScript + "\n" + script
        
        async def run_script(script):
            
            # Wait until there are processes available
            while self._nProcess>= self.maxProcesses:
                await asyncio.sleep(self.pollingTime)

            self._nProcess+=1
            proc= await asyncio.create_subprocess_shell(full_script,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE,shell=True)

            results=await proc.communicate()
            self._nProcess-=1

            if proc.returncode != 0:
                raise Exception(f"Script failed to run. Exit code: {proc.returncode}")
            
            
            return [ 
                result.decode("utf-8").strip() if (result is not None ) else None 
                for result in  results ] 
            #return [ result.decode("utdf-8").strip() for result in results if result is not None ]
        
        return asyncio.create_task( run_script(script) )

    

        
        

    


