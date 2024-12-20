# Add a pytest test case
from gridworld import GridWorld, Piece


def test_init():
    env = GridWorld(2, 2)
    assert env.width == 2
    assert env.height == 2
    assert env.player is not None
    assert len(env.pieces) == 3


def test_move():
    env = GridWorld(2, 2)
    env.player = (0, 0)
    env.pieces = {(1, 0): Piece.GOAL}
    assert env.move("r") == 10

    env.player = (0, 0)
    env.pieces = {(1, 0): Piece.PIT}
    assert env.move("r") == -10

    env.player = (0, 0)
    env.pieces = {(1, 0): Piece.WALL}
    assert env.move("r") == -5

    env.player = (0, 0)
    env.pieces = {}
    assert env.move("r") == -1


def test_render():
    env = GridWorld(2, 2)
    env.player = (0, 0)
    env.pieces = {(1, 0): Piece.GOAL, (1, 1): Piece.PIT, (0, 1): Piece.WALL}
    assert env.board == [[Piece.PLAYER, Piece.GOAL], [Piece.WALL, Piece.PIT]]
