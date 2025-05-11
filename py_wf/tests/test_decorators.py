from py_wf.executor.python import python_task
from py_wf.node import node
from py_wf.executor.shell import shell_task


def test_task_decorator():

    @node
    @python_task
    def world():
        return "World!"

    @node
    @python_task
    def hello(what):
        return "Hello " + what

    graph = hello(world())

    print(graph().output)


def test_slurm_task_decorator():

    @node
    @python_task
    def world():
        return "World"

    @node
    @shell_task
    def hello(word):
        return f"echo Hello {word}"

    graph = hello(world())

    assert graph().output[0] == "Hello World"
