from collections import deque
import asyncio
from py_wf.task import State
import copy


class Node:
    __used__names = set()

    @classmethod
    def get_available_name(cls, name: str) -> str:
        """Registers a new new unique name for a node

        Args:
            name:
                The propose new name for a node.
        Returns:
            A valid class name not yet in use
        """

        new_name = name
        i = 0
        while new_name in cls.__used__names:
            new_name = name + f"{i}"
            i += 1

        return new_name

    def __init__(self, name: str, task: object, dependencies=[], inputs=[]) -> None:
        """A node in a graph.

        Represents the node itself and the dependency tree for this node.

        Args:
            name:
                The name for this task. Needs to be unique.
            task:
                A task to execute. Needs to provide the __call__ method
            dependencies:
                A list of nodes that need to be executed before this node
                can be executed.

        """

        self.task = task
        self.__name = name

        if name in Node.__used__names:
            raise ValueError(
                f"""Node names needs to be unique.
                    Name {name} has already been used."""
            )
        else:
            Node.__used__names.add(name)

        self.__dependencies = []

        self.add_dependencies(dependencies)
        self.__set_input_nodes(inputs)

    def __set_input_nodes(self, nodes):

        self.__input_nodes = nodes
        for node in nodes:
            if node not in self.__dependencies:
                self.add_dependencies([node])

    def __eq__(self, node2) -> bool:
        return node2.name == self.name

    @property
    def output(self):
        return self.task.output

    @property
    def name(self):
        return copy.copy(self.__name)

    @property
    def state(self) -> State:
        return self.task.state

    @property
    def dependencies(self):
        """The number of direct dependencies of this node"""
        return self.__dependencies

    def add_dependencies(self, nodes):
        """Add a list of nodes as dependnecies"""

        for node in nodes:
            self.__dependencies.append(node)

    def __len__(self):
        """Return the number of nodes in this graph."""
        i = 0
        for node in self:
            i += 1
        return i

    def __call__(self):
        asyncio.run(self._run_async())
        return self

    def __del__(self):
        if self.name in Node.__used__names:
            Node.__used__names.remove(self.name)

    async def _run_async(self):
        """Run all the tasks in the graph.

        Dependencies are run before this node is needed.
        """

        # If nothing to do return self
        if self.state == State.FAILED or self.state == State.COMPLETED:
            return self

        results = await asyncio.gather(*[dep._run_async() for dep in self.dependencies])
        if any([result.state != State.COMPLETED for result in results]):
            self.state = State.FAILED
            return self

        inputs = [node.task.output for node in self.__input_nodes]
        await self.task(*inputs)

        return self

    def __repr__(self) -> str:
        return f"<Node name='{self.name}' state={self.state} task={self.task}>"

    def __iter__(self):
        return NodeIterator(self)


class NodeIterator:
    """Node Iterator.

    Uses Breath First Search to iterate overal all the dependencies in a tree.
    """

    def __init__(self, node) -> None:
        self.__de = deque()
        self.__de.append(node)
        self.__visited = set(node.name)

    def __next__(self) -> Node:

        if len(self.__de) == 0:
            raise StopIteration

        node = self.__de.popleft()
        for dep in node.dependencies:
            if dep.name not in self.__visited:
                self.__visited.add(dep.name)
                self.__de.append(dep)
        return node


def node(task_create):
    """Node creation decorator"""
    
    name = task_create.__name__

    def node_create(*inputs):
        task = task_create()
        new_node = Node(Node.get_available_name(name), task, inputs=inputs)
        return new_node

    return node_create
