import asyncio
import timeit

from py_wf.executor.shell import ShellExecutor
from py_wf.monitor import Monitor
from py_wf.node import Node
from py_wf.task import Task, State


def test_shell_executor_async():

    async def run_tasks():

        exec = ShellExecutor()

        bashMonitor = Monitor(exec)

        monitorTask = bashMonitor()
        tasks = [
            exec("sleep 5;echo Done1"),
            exec("sleep 5;echo Done2"),
            exec("sleep 5;echo Done3"),
        ]

        bashMonitor.enable()
        all_tasks = await asyncio.gather(*tasks)
        bashMonitor.disable()

        await monitorTask

        outputs = [task[0] for task in all_tasks]

        return outputs

    start = timeit.default_timer()
    outputs = asyncio.run(run_tasks())
    stop = timeit.default_timer()
    duration = stop - start
    assert (duration) <= 10
    assert (duration) >= 5

    assert outputs[0] == "Done1"
    assert outputs[1] == "Done2"
    assert outputs[2] == "Done3"


def test_shell_executor_node_dependencies():
    
    exec = ShellExecutor()
    dependencies = [
        Node(f"hello{i}", task=Task(f"echo Hello{1}! ", executor=exec))
        for i in range(10)
    ]
    node1 = Node(
        "trigger",
        task=Task("echo Trigger! ", executor=exec),
        dependencies=dependencies,
    )

    node1()

    assert node1.task.state == State.COMPLETED
