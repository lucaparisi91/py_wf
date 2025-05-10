from pathlib import Path
import os
import subprocess
from py_wf.executor.executor import Executor
from enum import Enum
import asyncio


class SlurmState(Enum):
    BOOT_FAIL = 1
    CANCELLED = 2
    COMPLETED = (3,)
    DEADLINE = (4,)
    FAILED = (5,)
    NODE_FAIL = (6,)
    OUT_OF_MEMORY = (7,)
    PENDING = (8,)
    PREEMPTED = (9,)
    RUNNING = (10,)
    SUSPENDED = (11,)
    TIMEOUT = 12


slurmFailedStates = set(
    [
        SlurmState.BOOT_FAIL,
        SlurmState.CANCELLED,
        SlurmState.DEADLINE,
        SlurmState.FAILED,
        SlurmState.NODE_FAIL,
        SlurmState.OUT_OF_MEMORY,
        SlurmState.PREEMPTED,
        SlurmState.TIMEOUT,
    ]
)

slurmCompletedStates = set([SlurmState.COMPLETED])


class SlurmExecutor(Executor):

    def __init__(
        self,
        preScript: str = "",
        maxProcesses: int = 4,
        default_resources={},
        polling_interval=10,
    ):
        self.preScript = preScript
        self.maxProcesses = maxProcesses
        self._nProcess = 0
        self.polling_interval = polling_interval
        self.default_resources = default_resources

    def __call__(
        self, script: str, work_dir: Path = Path("."), name="py_wf_job", resources={}
    ) -> asyncio.Task:

        work_dir = os.path.abspath(work_dir)

        async def submit_and_wait():
            # Prepare slurm batch flags

            slurm_options = dict()
            slurm_options.update(self.default_resources)

            slurm_options.update({"job-name": name})
            slurm_options.update(resources)

            # Generate a tempory batch script file
            batch_script = self._generate_batch_script(script, slurm_options, work_dir)
            script_file_name = os.path.join(work_dir, "submit.sh")
            with open(script_file_name, "w+") as f:
                f.write(batch_script)

            # Submit the script
            output = subprocess.check_output(
                ["sbatch", "--parsable", script_file_name], cwd=work_dir
            )
            job_id = int(output)

            # Wait until the job completes or fail
            state = None
            while state not in (slurmCompletedStates):
                await asyncio.sleep(self.polling_interval)
                state = self._get_state(job_id)

                if state in slurmFailedStates:
                    raise Exception(f"Job {job_id} failed")
            self.work_dir = work_dir

        return asyncio.create_task(submit_and_wait())

    def _get_state(self, job_id: int) -> SlurmState:
        """Return the slurm state given its jobid"""

        check_job_state = (
            f"sacct --parsable -j {job_id} "
            "--format=State | cut -d '|' -f1 | sed -n 2p"
        )
        state_output = subprocess.check_output(["sh", "-c", check_job_state])
        slurm_state_str = state_output.decode("utf-8").strip()
        slurm_state = SlurmState[slurm_state_str]

        return slurm_state

    def _generate_batch_script(
        self, script: str, slurm_options: dict, work_dir: Path = "."
    ) -> str:
        batch_script = "#!/bin/bash\n"

        for option_name, option_value in slurm_options.items():
            batch_script += f"#SBATCH --{option_name}={option_value}\n"

        if work_dir is not None:
            batch_script += f"cd {work_dir}\n"
        batch_script += script

        return str(batch_script)
