import asyncio


class Monitor:

    def __init__(self,executor,name=None) -> None:
        self._enabled=True
        self.executor=executor
        self.pollingTime=1
        self.name=name
        self._running=False

        if name is None:
            self.name=self.name=type(executor).__name__

    def enable(self):
        """Enable monitoring

        Any co-rutine generated from this object will start printing to the screen once invoked
        """
        self._enabled=True

    def disable(self):
        """ Terminates monitoring from any co-routine currently being awaited
        """
        self._enabled=False


    def __call__(self) -> asyncio.Task:
        """ Returns an asynchroneous task responsible for running the monitoring
        """
        return asyncio.create_task( self._monitor() )

    async def _monitor(self):
        
        while self._enabled:
            if not self._running:
                print(f"{self.name}> Start monitoring")
                self._running=True
            print(f"\r{self.name}> Processes: {self.executor._nProcess}/{self.executor.maxProcesses}",end="\r")
            await asyncio.sleep(self.pollingTime)
        self._running=True        
        print(f"\n{self.name}> End monitoring")
