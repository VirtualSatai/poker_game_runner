import numpy as np
from typing import List

from poker_game_runner.state import Observation

class Bot:

    def __init__(self, actions: List[int]) -> None:
        self.counter = 0
        self.actions = actions

    def get_name(self):
        return "testBot"

    def act(self, obs: Observation):
        action = self.actions[self.counter]
        self.counter += 1
        return action