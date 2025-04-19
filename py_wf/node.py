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
    
    @property
    def dependencies(self):
        """The number of direct dependencies of this node
        """
        return self.__dependencies

    def addDependencies(self,nodes ):
        """Add a list of nodes as dependnecies
        """

        for node in nodes:
            self.__dependencies.append(node)
    

    def __len__(self):
        """ Return the number of nodes in this graph.
        """
        i= 0
        for node in self:
              i+=1
        return i

    def runTask(self):
        self.state=self.task()
        return self

    def __call__(self) :
        """Run all the tasks in the graph. Dependencies are run before this node is needed.
        """

        # If nothing to do return self
        if self.state == State.FAILED or self.state == State.COMPLETED:
            return self
        

        
        dependenciesSatisfied=True
        for dep in self.dependencies:
            # Run the dependency
            depState=dep().state
            # If any of the dependencies have failed , fail this task
            if depState == State.FAILED:
                self.state=State.FAILED
                return self
            dependenciesSatisfied=dependenciesSatisfied and (depState==State.COMPLETED)

        if dependenciesSatisfied:
            try: 
                self.task()
            except:
                self.state==State.FAILED
            else:
                self.state=State.COMPLETED
        else:
            self.state = State.DEPENDENCIES
        
        return self


    def __repr__(self) -> str:
        return f"<Node name='{self.name}', state={self.state}>"

    def __iter__(self):
        return NodeIterator(self)


class NodeIterator:
    """Node Iterator. Uses Breath First Search to iterate overal all the dependencies in a tree.
    """

    def __init__(self,node) -> None:
        self.__de = deque()
        self.__de.append(node)
        self.__visited=set()

    def __next__( self ) -> Node :
        
        if len(self.__de)==0:
            raise StopIteration

        node = self.__de.pop()

        self.__visited.add(node.name)

        for dep in node.dependencies:
            if dep not in self.__visited:
                self.__de.append(dep)

        return node