import numpy as np
from Game.game import Game


class AIPlayer:

    def __init__(self, game, weights, bias):
        self.weights = np.array(weights)
        self.bias = bias
        self.game = game

    def next_move(self):
        pass

