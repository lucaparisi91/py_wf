import asyncio
import timeit



from py_wf.executor import ShellExecutor
from py_wf.monitor import Monitor

def test_shel_executor_async():

    async def run_tasks():

        
        exec=ShellExecutor()
        
        bashMonitor=Monitor(exec)
        
        monitorTask=bashMonitor( )
        tasks = [
            exec("sleep 5;echo Done1"),
            exec("sleep 5;echo Done2"),
            exec("sleep 5;echo Done3")
        ]

        bashMonitor.enable()
        all_tasks=await asyncio.gather(*tasks)
        bashMonitor.disable()

        await monitorTask


        outputs= [ task[0].decode("utf-8").strip() for task in all_tasks]
        
        return outputs

    start =  timeit.default_timer()
    outputs=asyncio.run(run_tasks() )
    stop= timeit.default_timer()
    duration= stop - start
    assert((duration)<=10 )
    assert((duration)>=5 )

    assert(outputs[0]== "Done1")
    assert(outputs[1]== "Done2")
    assert(outputs[2]== "Done3")