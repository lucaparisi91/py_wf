
from py_wf.task import Task, State
from py_wf.executor import ShellExecutor , PythonExecutor
import asyncio

def test_run_async():
    executor=ShellExecutor()
    task = Task("sleep 1 ;echo Hello!", executor=executor )

    
    asyncio.run( task() )

    assert( task.state == State.COMPLETED )

    assert (    task.output[0] == "Hello!" )
    

def test_run_fail():
    executor=ShellExecutor()
    task = Task("sleep(10)", executor=executor )
    
    asyncio.run( task() )

    assert( task.state == State.FAILED )


def test_python_executor():

    executor=PythonExecutor()

    def hello():
        return "Hello"
    
    task = Task( hello, executor=executor )

    asyncio.run(task() )

    assert(task.output == "Hello" )

