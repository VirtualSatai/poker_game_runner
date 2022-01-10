import numpy as np

def getName():
    return "randomBot"

def act(state, legal_actions):
    return np.random.choice(state.legal_actions())