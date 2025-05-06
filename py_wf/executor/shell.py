import asyncio
from py_wf.executor.executor import Executor


class ShellExecutor(Executor):

    def __init__(self, preScript: str = "", maxProcesses: int = 4):
        self.preScript = preScript
        self.maxProcesses = maxProcesses
        self._nProcess = 0
        self.pollingTime = 1

    def __call__(self, script: str) -> asyncio.Task:
        full_script = self.preScript + "\n" + script

        async def run_script(script):

            # Wait until there are processes available
            while self._nProcess >= self.maxProcesses:
                await asyncio.sleep(self.pollingTime)

            self._nProcess += 1
            proc = await asyncio.create_subprocess_shell(
                full_script,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True,
            )

            results = await proc.communicate()
            self._nProcess -= 1

            if proc.returncode != 0:
                raise Exception(f"""Script failed to run.
                                   Exit code: {proc.returncode}""")

            return [
                result.decode("utf-8").strip()
                if (result is not None) else None
                for result in results
            ]

        return asyncio.create_task(run_script(script))
