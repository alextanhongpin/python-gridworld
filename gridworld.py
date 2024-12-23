import random

from enum import StrEnum


class Piece(StrEnum):
    EMPTY = "."
    GOAL = "+"
    OVERLAP = "X"
    PIT = "-"
    PLAYER = "P"
    WALL = "W"


class Direction(StrEnum):
    UP = "u"
    DOWN = "d"
    LEFT = "l"
    RIGHT = "r"



Coords = complex


class GridWorld:
    MOVES = {
        Direction.UP: complex(0, -1),
        Direction.DOWN: complex(0, 1),
        Direction.LEFT: complex(-1, 0),
        Direction.RIGHT: complex(1, 0),
    }
    PIECES = [Piece.GOAL, Piece.PIT, Piece.WALL, Piece.PLAYER]
    REWARDS = {
        Piece.GOAL: +10,
        Piece.PIT: -10,
    }

    def __init__(self, size=2):
        assert size >= 2, "size must be at least 2"
        self.size = size
        self.pieces = {}
        self.reset()

    @property
    def board(self):
        player, others = self.scan(self.pieces)
        rows = []
        for y in range(self.size):
            cols = []
            for x in range(self.size):
                pos = complex(x, y)
                if pos == player and player in others:
                    cols.append(Piece.OVERLAP)
                elif pos == player:
                    cols.append(Piece.PLAYER)
                elif pos in others:
                    cols.append(others[pos])
                else:
                    cols.append(Piece.EMPTY)
            rows.append(cols)
        return rows

    def render(self):
        for rows in self.board:
            print("".join(rows))

    def move(self, direction: Direction) -> int:
        """
        Move the player in the given direction and return the reward.
        Every non-winning move has a reward of -1.
        Goal has a reward of +10, pit has a reward of -10.
        Player cannot step on the wall or outside of the boundary.
        """

        assert (
            direction in self.MOVES
        ), f"direction must be one of {', '.join(self.MOVES.keys())}, got: {direction}"

        curr, others = self.scan(self.pieces)
        next = self.MOVES[direction] + curr
        if not self.is_in_boundary(next) or others.get(next) == Piece.WALL:
            return -1

        self.pieces[Piece.PLAYER] = next
        return self.REWARDS.get(others.get(next), -1) 

    def reset(self):
        while True:
            coords = self.random_coords(len(self.PIECES))
            pieces = dict(zip(self.PIECES, coords))
            if self.validate_board(pieces):
                self.pieces = pieces
                break

    def random_coords(self, n: int):
        assert n <= self.size * self.size, "n must be less than the number of tiles"

        coords = set[Coords]()
        while len(coords) != n:
            x = random.randrange(0, self.size)
            y = random.randrange(0, self.size)
            coords.add(complex(x, y))

        return list(coords)

    def validate_board(self, coords_by_piece: dict[Piece, Coords]) -> bool:
        """
        Validate the board to make sure it is solvable.
        Performs a BFS from the player's position to see if it can reach the goal.
        """
        player, pieces = self.scan(coords_by_piece)
        queue = [player]

        visited = set()
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            match pieces.get(curr, Piece.EMPTY):
                case Piece.GOAL:
                    return True
                case Piece.WALL, Piece.PIT:
                    continue
            for move in self.MOVES.values():
                next = curr + move
                if not self.is_in_boundary(next):
                    continue
                queue.append(next)
        return False

    def is_in_boundary(self, coords: Coords):
        return 0 <= coords.real < self.size or 0 <= coords.imag < self.size

    def scan(self, pieces: dict[Piece, Coords]) -> tuple[Coords, dict[Coords, Piece]]:
        player = pieces[Piece.PLAYER]
        others = {v: k for k, v in pieces.items() if k != Piece.PLAYER}
        return player, others
