# Workflow manager

This is meant to be a light-way pythton script to manage workflows for benchmarking purposes.

- Dynamic execution can be done by creating a sub-dag and executing it in a task.

## Example: Run a simulation on multiple nodes

```python

nodes=[1,2,3,4]
runs=[]

for node in nodes:

    script="echo $(hostname) > name-{node}.txt"

    @task.bash(executor=slurm_executor,resources={"nodes":1},script=script )
    def run(node):
        return "name-{node}.txt"
    
    runs.append(run(node) )

report=collect(runs)

report()

```
```python