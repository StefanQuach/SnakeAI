import numpy as np
from AI.AI_Player import AIPlayer
from Game.game import Game
import struct


class Trainer:
    def __init__(self, gen_size=100, threshold=10):
        self.games = [Game(fps=100, caption='Game '+str(x)) for x in range(gen_size)]
        self.curr_gen = [AIPlayer(x, [10, 10], random=True) for x in self.games]
        self.gen_size = gen_size
        self.threshold = threshold
    # TODO score using 50*game.score + time lived
    # TODO some way to stop the game if just going in circles
    #   record last time score was updated, measure how long since then, if too long, end game


def breed(a, b):
    child_a_weight = []
    for a_matrix, b_matrix in zip(a.weights, b.weights):
        for a_row, b_row in zip(a.weights[a_matrix], b.weights[b_matrix]):
            # do some crossing over?
            # bitwise crossing over
            pass


def cross_over(num1, num2):
    p = np.rand()
    temp1 = float_to_bits(num1)
    temp2 = float_to_bits(num2)


def float_to_bits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]


def bits_to_float(b):
    s = struct.pack('>l', b)
    return struct.unpack('>f', s)[0]


if __name__ == "__main__":
    a = np.matrix([[4, 5], [6, 7]])
    for i in a:
        print(i)
