from typing import Protocol

Action = int
Info = dict[str, int]
Matrix = list[list[int]]
Observation = list[Matrix]
Reward = int
Terminated = bool
Truncated = bool


class Environment(Protocol):
    @property
    def action_space(self) -> list[int]:
        pass

    @property
    def observation_space(self) -> tuple[int, int]:
        pass

    def reset(self, seed=None) -> tuple[Observation, Info]:
        pass

    def step(
        self, action: int
    ) -> tuple[Observation, Reward, Terminated, Truncated, Info]:
        pass
