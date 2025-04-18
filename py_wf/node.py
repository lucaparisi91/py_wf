from enum import Enum
from collections import deque

class State(Enum):
    COMPLETED = 0
    FAILED = 1
    DEPENDENCIES = 2


class Node:
    __used__names=set()

    def __init__(self,name: str,task: object, dependencies= []) -> None:
        """ A node in a graph. Represents the node itself and the dependency tree for this node.

        Args:
            name:
                The name for this task. Needs to be unique.
            task:
                A task to execute. Needs to provide the __call__ method
            dependencies:
                A list of nodes that need to be executed before this node can be executed.

        """
        
        self.task=task
        self.state=None

        if name in Node.__used__names:
            raise ValueError(f"Node names needs to unique. Name {name} has alreaddy been used.")
        else:
            Node.__used__names.add(name)

        self.name=name
        self.__dependencies=[]

        self.addDependencies(dependencies)
        

    def addDependencies(self,nodes ):
        """Add a list of nodes as dependnecies
        """

        for node in nodes:
            self.__dependencies.append(node)
    

    def __len__(self):
        """ Return the namber of nodes in this graph
        """
        pass 
    
    def __call__(self) -> None:
        """Run all the tasks in the graph. Dependencies are run before this node is needed.
        """

        self.state=State.DEPENDENCIES
        pass 
        
        # for dep in dependencies:
        #     if dep.state is not None:
        #         dep()

        # self.state=State.SUBMITTED
        # self.state=self.task()
    


class NodeIterator:

    def __init__(self,node) -> None:
        self.__de = deque(node)
        self.__visited=set()

    def __next__( self ) -> Node :
        
        if len(self.__de)==0:
            raise StopIteration

        node = self.__de.pop()

        self.__visited.add(node.name)

        for dep in self.dependencies:
            if dep not in self.__visited:
                self.__de.append(dep)

        return node