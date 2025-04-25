from typing import Any
from subprocess import check_output, STDOUT
import asyncio 


class PythonExecutor:
    def __init__(self):
        pass
    
    async def __call__(self,func,*args,**kwds) -> Any:
        
        return func(*args,**kwds)

class ShellExecutor:
    

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
            proc= await asyncio.create_subprocess_shell(full_script,stdout=asyncio.subprocess.PIPE,shell=True)

            results=await proc.communicate()
            self._nProcess-=1

            return results

        return asyncio.create_task( run_script(script) )

    

        
        

    


