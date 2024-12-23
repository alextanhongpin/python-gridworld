# Add a pytest test case
from gridworld import GridWorld, Piece


def test_init():
    env = GridWorld(2)
    assert env.size == 2
    assert len(env.pieces) == 4


def test_move():
    env = GridWorld(2)
    env.pieces = {
        Piece.PLAYER: complex(0, 0),
        Piece.GOAL: complex(1, 0),
    }
    assert env.move("r") == 10

    env.pieces = {
        Piece.PLAYER: complex(0, 0),
        Piece.PIT: complex(1, 0),
    }
    assert env.move("r") == -10

    env.pieces = {
        Piece.PLAYER: complex(0, 0),
        Piece.WALL: complex(1, 0),
    }
    assert env.move("r") == -1

    env.pieces = {Piece.PLAYER: complex(0, 0)}
    assert env.move("r") == -1


def test_render():
    env = GridWorld(2)
    env.pieces = {
        Piece.PLAYER: complex(0, 0),
        Piece.GOAL: complex(1, 0),
        Piece.PIT: complex(1, 1),
        Piece.WALL: complex(0, 1),
    }
    assert env.board == [[Piece.PLAYER, Piece.GOAL], [Piece.WALL, Piece.PIT]]
