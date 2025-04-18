
# Python Workflow manager

## Testing

```bash

source env.sh
pytest -vvv --capture=tee-sys py_wf/tests/

```

## Workflow manager Design

This is meant to be a light-way pythton script to manage workflows for benchmarking purposes.

- Dynamic execution can be done by creating a sub-dag and executing it in a task.

## Example: Create a python task dependencies

```python

@task
def greeting_italian():
    
    return "Ciao!"

@task
def greeting_french():
    
    return "Bonjour!"

@task
def all_greetings(italian_greeting,french_greeting):
    return f"{italian_greeting} & {french_greeting}"


greet=all_greetings(greeting_italian,greeting_french)
greet()

```

## Example : run a bash script and parse the output

```python
@bash
def greet_hostname(greeting):
    return f"echo {greeting} $(hostname)"

@task
def say_hello():

    greet_hostname("Ciao")

    print("OK")

task=say_hello()
task()

```
