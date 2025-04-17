class node:
    
    def __init__(self,task,dependencies=[]) -> None:
        self._parents=[]
        self.task=task
        self.state=None
        for dep in dependencies:
            self.__add_dependency(self)

    def __next__(self):

        

    def __add_dependency(self,depency: node) -> None:

        self.__parents.append(depency)

    def __call__(self) -> None:

        self.task()
        for parent in self._parents:
            if parent.state is not None:
                parent()