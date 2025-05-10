from py_wf.executor.slurm import SlurmExecutor
from py_wf.task import Task
import asyncio


def test_slurm_executor():

    executor = SlurmExecutor(
        default_resources={
            "nodes": 1,
            "cpus-per-task": 1,
            "qos": "short",
            "partition": "standard",
            "time": "00:20:00",
            "account": "n02-NGARCH",
        }
    )

    async def run_script():
        script = "echo Hello!"

        await executor(script, resources={"output": "hello.out"})

    asyncio.run(run_script())

    with open("hello.out") as f:
        assert f.read().strip() == "Hello!"


def test_slurm_executor_task():

    executor = SlurmExecutor(
        default_resources={
            "nodes": 1,
            "cpus-per-task": 1,
            "qos": "short",
            "partition": "standard",
            "time": "00:20:00",
            "account": "n02-NGARCH",
        }
    )

    task = Task("echo Hello!", resources={"output": "hello2.out"}, executor=executor)

    asyncio.run(task())

    with open("hello2.out") as f:
        assert f.read().strip() == "Hello!"
