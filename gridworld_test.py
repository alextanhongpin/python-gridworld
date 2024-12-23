# Add a pytest test case
from gridworld import GridWorld, Piece


def test_init():
    env = GridWorld(2, 2)
    assert env.width == 2
    assert env.height == 2
    assert len(env.pieces) == 4


def test_move():
    env = GridWorld(2, 2)
    env.pieces = {
        Piece.PLAYER: (0, 0),
        Piece.GOAL: (1, 0),
    }
    assert env.move("r") == 10

    env.pieces = {
        Piece.PLAYER: (0, 0),
        Piece.PIT: (1, 0),
    }
    assert env.move("r") == -10

    env.pieces = {
        Piece.PLAYER: (0, 0),
        Piece.WALL: (1, 0),
    }
    assert env.move("r") == -5

    env.pieces = {Piece.PLAYER: (0, 0)}
    assert env.move("r") == -1


def test_render():
    env = GridWorld(2, 2)
    env.pieces = {
        Piece.PLAYER: (0, 0),
        Piece.GOAL: (1, 0),
        Piece.PIT: (1, 1),
        Piece.WALL: (0, 1),
    }
    assert env.board == [[Piece.PLAYER, Piece.GOAL], [Piece.WALL, Piece.PIT]]
