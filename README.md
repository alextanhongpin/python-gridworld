# python-gridworld


> [!IMPORTANT]  
> The repository name cannot contain `-` dash for it to be a valid python module.

Build:

```bash
$ poetry build
```

Import:

```bash
poetry add git+https://github.com/alextanhongpin/python_gridworld.git
```

```python
from gridworld.gridworld import GridWorld
env = GridWorld(4)
env.reset(seed=None)
print(env.render())

# 0: up, 1: right, 2: down, 3: left
observation, reward, terminated, truncated, info = env.step(0) 
```
