# python-gridworld

Build:

```bash
$ poetry build
```

Import:

```bash
poetry add https://github.com/alextanhongpin/python-gridworld.git
```

```python
from gridworld import GridWorld, Piece
env = GridWorld(4)
print(env.render())
```
