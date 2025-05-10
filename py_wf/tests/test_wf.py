import asyncio 
from py_wf.task import python_task
from py_wf.node import node

def test_task_decorator():

    @node
    @python_task
    def world():
        return "World!"

    @node
    @python_task
    def hello(what):
        return "Hello " + what
    


    #task = world()
    #asyncio.run( task() )

    #print(task.output)
    #returned = asyncio.run(world()() )

    #assert returned == "Hello World!"

