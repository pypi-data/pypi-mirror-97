# `reequirements`

`reequirements` is a useful library for defining and checking for the status of (not necessarily Python) requirements needed for your Python project.

## Usage

Create some `Requirement` objects. Specify a friendly name for the requirement, a command to be able to check that requirement, and if it should issue a warning or halt the program if it is missing.

```python
from reequirements import Requirement

REQUIREMENTS = [
    Requirement("docker", ["docker", "-v"], warn=False)
    Requirement("fortune", ["fortune", "-v"], warn=True)
]
```

Now, iterate through these requirements and check them.

```python
for r in REQUIREMENTS:
    r.check()
```

`RequirementMissing` will be raised if `docker -v` exits with exit code 127 (command not found), or the more generic `RequirementError` will be raised if it exits with any other nonzero exit code.

`RequirementMissingWarning` will be warned if `fortune -v` exits with exit code 127 (command not found), or the more generic `RequirementErrorWarning` will be warned if it exits with any other nonzero exit code.

## Tips

- Make sure your commands to check requirements end with the correct exit code! This often means using flags like `-v`, `-h` when it comes to command line tools

- You do not need to check for requirements right away; you can create `Requirement` at any time and check it whenever you want
