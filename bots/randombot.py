import numpy as np

from InfoState import Observation

def get_name():
    return "randomBot"

def act(observation: Observation):
    return np.random.choice(observation.legal_actions)