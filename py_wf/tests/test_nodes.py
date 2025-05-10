from py_wf.node import Node
from py_wf.executor.python import PythonExecutor
from py_wf.task import Task


def test_node():

    executor = PythonExecutor()

    def dummy_task1():
        return "Hello 1 !"

    def dummy_task2():
        return "Hello 2 !"

    def dummy_task3():
        return "Hello 3 !"

    node1 = Node("hello1", task=Task(dummy_task1, executor=executor))
    node2 = Node("hello2", task=Task(dummy_task2, executor=executor))

    # check wether non unique names raise an error
    try:
        Node("hello2", task=dummy_task2)
    except ValueError:
        pass
    else:
        raise Exception("Non unique task name should have raised an error")

    node3 = Node(
        "hello3", task=Task(dummy_task3, executor=executor), dependencies=[node1, node2]
    )

    assert node3.dependencies[0].name == node1.name
    assert node3.dependencies[1].name == node2.name

    assert len(node3) == 3

    for node in node3:
        assert node.name in set(["hello1", "hello2", "hello3"])

    node3()

    assert node1.task.output == "Hello 1 !"
    assert node2.task.output == "Hello 2 !"
    assert node3.task.output == "Hello 3 !"


def test_dyamond():

    executor = PythonExecutor()

    def dummy_task(n):
        def dummy():
            return f"Hello {n} !"

        return dummy

    node0 = Node("hello0d", task=Task(dummy_task(0), executor=executor))
    node1 = Node(
        "hello1d", task=Task(dummy_task(1), executor=executor), dependencies=[node0]
    )

    node2 = Node(
        "hello2d", task=Task(dummy_task(2), executor=executor), dependencies=[node0]
    )
    node3 = Node(
        "hello3d",
        task=Task(dummy_task(3), executor=executor),
        dependencies=[node1, node2],
    )

    expected_order = ["hello3d", "hello1d", "hello2d", "hello0d"]

    assert len(node3) == 4

    for i, node in enumerate(node3):
        assert node.name == expected_order[i]

    node3()

    assert node3.task.output == "Hello 3 !"
    assert node1.task.output == "Hello 1 !"
    assert node2.task.output == "Hello 2 !"


def test_chaining():

    executor = PythonExecutor()

    def world():
        return "World!"

    def hello(word):
        return f"Hello {word}"

    node0 = Node("world", task=Task(world, executor=executor))
    node1 = Node("hello", task=Task(hello, executor=executor), inputs=[node0])

    node1()

    assert node1.task.output == "Hello World!"
