# python-gridworld


> [!IMPORTANT]  
> The repository name cannot contain `-` dash for it to be a valid python module.

Build:

```bash
$ poetry build
```

Import:

```bash
poetry add https://github.com/alextanhongpin/python_gridworld.git
```

```python
from gridworld import GridWorld, Piece
env = GridWorld(4)
print(env.render())
```
