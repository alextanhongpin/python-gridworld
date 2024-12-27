from env import Environment, Info, Reward, Terminated, Truncated, Observation
from collections import defaultdict
import random


class GridWorld(Environment):
    ACTIONS = [0, 1, 2, 3]  # up, down, left and right
    MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left and right
    PIECES = ["P", "+", "-", "W"]
    coords: list[tuple[int, int]] = []

    def __init__(self, size=2):
        assert size >= 2, "size must be at least 2"
        self.size = size

    @property
    def action_space(self) -> list[int]:
        return self.ACTIONS

    @property
    def observation_space(self) -> tuple[int, int]:
        return self.size, self.size

    def reset(self, seed=None) -> tuple[Observation, Info]:
        random.seed(seed)

        while True:
            # Generate random positions for each piece.
            coords = set[tuple[int, int]]()
            while len(coords) != len(self.PIECES):
                x = random.randrange(0, self.size)
                y = random.randrange(0, self.size)
                coords.add((x, y))

            coords = list(coords)
            if self.validate_board(coords[:]):
                self.coords = coords
                break
        return self.observation, self.info

    def step(
        self, action: int
    ) -> tuple[Observation, Reward, Terminated, Truncated, Info]:
        assert action in self.ACTIONS, "invalid action"
        player, others = self.coords[0], self.coords[1:]

        move = self.MOVES[action]
        next = tuple(map(sum, zip(player, move)))
        if self.is_oob(next):
            return self.observation, -1, False, self.truncated, self.info

        self.coords[0] = next

        if next in others:
            piece = self.PIECES[others.index(next) + 1]
            if piece == "+":
                return self.observation, +10, True, self.truncated, self.info
            if piece in "-":
                return self.observation, -10, True, self.truncated, self.info
        return self.observation, -1, False, self.truncated, self.info

    @property
    def observation(self) -> Observation:
        result = []
        for coord in self.coords:
            matrix = [[0] * self.size for y in range(self.size)]
            r, c = coord
            matrix[r][c] = 1
            result.append(matrix)
        return result

    @property
    def truncated(self) -> bool:
        return False

    @property
    def info(self) -> dict:
        return {}

    def validate_board(self, coords: list[tuple[int, int]]) -> bool:
        """
        Validate the board to make sure it is solvable.
        Performs a BFS from the player's position to see if it can reach the goal.
        """
        player = coords[0]
        others = coords[1:]
        queue = [player]

        visited = set()
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)

            if self.is_oob(curr):
                continue

            if curr in others:
                piece = self.PIECES[others.index(curr) + 1]
                if piece == "+":
                    return True
                if piece in "-W":
                    continue
            for move in self.MOVES:
                next = tuple(map(sum, zip(curr, move)))
                queue.append(next)

        return False

    def is_oob(self, coord: tuple[int, int]) -> bool:
        return not (0 <= coord[0] < self.size and 0 <= coord[1] < self.size)

    def render(self):
        obs = dict(list(zip(self.coords, self.PIECES))[::-1])
        rows = []
        for r in range(self.size):
            cols = []
            for c in range(self.size):
                if (r, c) in obs:
                    cols.append(obs[(r, c)])
                else:
                    cols.append(".")
            rows.append(cols)
        return rows
