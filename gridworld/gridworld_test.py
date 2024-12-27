# Add a pytest test case
from .gridworld import GridWorld


def make():
    env = GridWorld(2)
    env.coords = [None] * 4
    env.coords[0] = (0, 0)  # Player, top left
    env.coords[1] = (0, 1)  # Goal, top right
    env.coords[2] = (1, 0)  # Pit, bottom left
    env.coords[3] = (1, 1)  # Wall, bottom right

    return env


def test_init():
    env = GridWorld(2)
    assert env.size == 2
    assert len(env.coords) == 0
    env.reset()
    assert len(env.coords) == 4
    assert env.action_space == [0, 1, 2, 3]
    assert env.observation_space == (2, 2)


def test_step_goal():
    env = make()
    observation, reward, terminated, truncated, info = env.step(3)
    assert observation == [
        [[0, 1], [0, 0]],
        [[0, 1], [0, 0]],
        [[0, 0], [1, 0]],
        [[0, 0], [0, 1]],
    ]
    assert reward == +10
    assert terminated
    assert not truncated
    assert info == {}


def test_step_pit():
    env = make()
    observation, reward, terminated, truncated, info = env.step(1)
    assert observation == [
        [[0, 0], [1, 0]],
        [[0, 1], [0, 0]],
        [[0, 0], [1, 0]],
        [[0, 0], [0, 1]],
    ]
    assert reward == -10
    assert terminated
    assert not truncated
    assert info == {}


def test_step_wall():
    env = GridWorld(2)
    env.coords = [None] * 4
    env.coords[0] = (0, 0)  # Player, top left
    env.coords[1] = (1, 0)  # Goal, bottom left
    env.coords[2] = (1, 1)  # Pit, bottom right
    env.coords[3] = (0, 1)  # Wall, top right

    observation, reward, terminated, truncated, info = env.step(3)
    assert observation == [
        [[0, 1], [0, 0]],
        [[0, 0], [1, 0]],
        [[0, 0], [0, 1]],
        [[0, 1], [0, 0]],
    ]
    assert reward == -1
    assert not terminated
    assert not truncated
    assert info == {}


def test_step_large():
    env = GridWorld(3)
    env.reset(seed=42)

    # The shortest path is right, right, up.
    assert env.render() == [
        ["W", ".", "+"],
        ["P", ".", "."],
        ["-", ".", "."],
    ]
    _observation, reward, terminated, _truncated, _info = env.step(3)
    assert reward == -1
    assert not terminated

    _observation, reward, terminated, _truncated, _info = env.step(3)
    assert reward == -1
    assert not terminated

    _observation, reward, terminated, _truncated, _info = env.step(0)
    assert reward == +10
    assert terminated
