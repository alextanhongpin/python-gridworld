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


Coords = tuple[int, int]


class GridWorld:
    MOVES = {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0),
    }
    PIECES = [Piece.GOAL, Piece.PIT, Piece.WALL, Piece.PLAYER]

    def __init__(self, width, height):
        assert width >= 2 and height >= 2, "width and height must be at least 2"

        self.width = width
        self.height = height
        self.pieces = {}
        self.reset()

    @property
    def board(self):
        player, others = self.scan(self.pieces)
        rows = []
        for y in range(self.height):
            cols = []
            for x in range(self.width):
                pos = (x, y)
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
        assert (
            direction in self.MOVES
        ), f"direction must be one of {', '.join(self.MOVES.keys())}, got: {direction}"

        player, others = self.scan(self.pieces)
        px, py = player
        dx, dy = self.MOVES[direction]
        nx, ny = px + dx, py + dy
        if not self.is_in_boundary((nx, ny)):
            return 0

        self.pieces[Piece.PLAYER] = (nx, ny)

        if (nx, ny) in others:
            match others[(nx, ny)]:
                case Piece.GOAL:
                    return +10
                case Piece.PIT:
                    return -10
                case Piece.WALL:
                    return -5
                case _:
                    return -1
        return -1

    def reset(self):
        while True:
            coords = self.random_coords(len(self.PIECES))
            pieces = dict(zip(self.PIECES, coords))
            if self.validate_board(pieces):
                self.pieces = pieces
                break

    def random_coords(self, n: int):
        assert n <= self.width * self.height, "n must be less than the number of tiles"

        coords = set[tuple[int, int]]()
        while len(coords) != n:
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
            coords.add((x, y))

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
            p = queue.pop(0)
            if p in visited:
                continue
            visited.add(p)
            match pieces.get(p, Piece.EMPTY):
                case Piece.GOAL:
                    return True
                case Piece.WALL, Piece.PIT:
                    continue
            px, py = p
            for dx, dy in self.MOVES.values():
                nx = px + dx
                ny = py + dy
                if not self.is_in_boundary((nx, ny)):
                    continue
                queue.append((nx, ny))
        return False

    def is_in_boundary(self, coords):
        x, y = coords
        return 0 <= x < self.width and 0 <= y < self.height

    def scan(self, pieces: dict[Piece, Coords]) -> tuple[Coords, dict[Coords, Piece]]:
        player = pieces[Piece.PLAYER]
        others = {v: k for k, v in pieces.items() if k != Piece.PLAYER}
        return player, others
