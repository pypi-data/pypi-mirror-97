# shell-cmd Python package

Simple wrapper for executing shell commands using just one Python function.

## Installation

```
$ pip install shell_cmd
```

## Example

```
from shell_cmd import sh


# Printing output
print(sh("ls -l"))

# Getting output in a list
ll = sh("ls -l", True)
```

If error happens during the execution of the shell command, then `RunShellException`
custom exception is raised.

