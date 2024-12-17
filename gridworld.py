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


class GridWorld:
    MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
    DIRECTIONS = list(map(str, Direction))
    PIECES = [Piece.GOAL, Piece.PIT, Piece.WALL, Piece.PLAYER]

    def __init__(self, width, height):
        assert width >= 2 and height >= 2, "width and height must be at least 2"

        self.width = width
        self.height = height
        self.player = None
        self.pieces = {}
        self.reset()

    @property
    def board(self):
        rows = []
        for y in range(self.height):
            cols = []
            for x in range(self.width):
                if (x, y) == self.player:
                    if self.player in self.pieces:
                        cols.append(Piece.OVERLAP)
                    else:
                        cols.append(Piece.PLAYER)
                elif (x, y) in self.pieces:
                    cols.append(self.pieces[(x, y)])
                else:
                    cols.append(Piece.EMPTY)
            rows.append(cols)
        return rows

    def render(self):
        for rows in self.board:
            print("".join(rows))

    def move(self, direction: Direction) -> int:
        assert (
            direction in self.DIRECTIONS
        ), f"direction must be one of {', '.join(self.DIRECTIONS)}, got: {direction}"

        x, y = self.player
        dx, dy = self.MOVES[self.DIRECTIONS.index(direction)]
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
            return 0

        self.player = nx, ny
        match self.pieces.get(self.player):
            case Piece.GOAL:
                return +10
            case Piece.PIT:
                return -10
            case Piece.WALL:
                return -5
            case _:
                return -1

    def reset(self):
        while True:
            coords = self.random_coords(len(self.PIECES))
            pieces = dict(zip(self.PIECES, coords))
            player = pieces[Piece.PLAYER]
            del pieces[Piece.PLAYER]
            pieces = {v: k for k, v in pieces.items()}
            if self.validate_board(player, pieces):
                self.player = player
                self.pieces = pieces
                break

    def random_coords(self, n: int):
        assert n <= self.width * self.height, "n must be less than the number of tiles"

        grid = set[tuple[int, int]]()
        while len(grid) != n:
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
            grid.add((x, y))

        return list(grid)

    def validate_board(self, player, pieces):
        """
        Validate the board to make sure it is solvable.
        Performs a BFS from the player's position to see if it can reach the goal.
        """
        queue = [player]

        visited = set()
        while queue:
            head, queue = queue[0], queue[1:]
            if head in visited:
                continue
            visited.add(head)
            p = pieces.get(head, Piece.EMPTY)
            if p == Piece.GOAL:
                return True
            if p == Piece.WALL or p == Piece.PIT:
                continue
            x, y = head
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx = x + dx
                ny = y + dy
                if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                    continue
                queue.append((nx, ny))
        return False
