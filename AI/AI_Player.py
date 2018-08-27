import numpy as np


class AIPlayer:

    def __init__(self, game, hidden_neurons, weights=None, bias=None, random=False):
        self.game = game
        neurons = [20, *hidden_neurons, 3]
        # TODO implement a check if weights and biases are correct shape
        if random:
            self.bias = [np.random.randn(y, 1) for y in neurons[1:]]
            self.weights = [np.random.randn(y, x) for x, y in zip(neurons[:-1], neurons[1:])]
        else:
            self.weights = weights
            self.bias = bias

    def output(self, a):
        for b, w in zip(self.bias, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def next_move(self):
        # TODO maybe check diagonal direction too
        straight = self.game.player.direction
        backwards = -1*straight
        right = np.cross(straight, np.array([0, 0, 1]))
        left = np.cross(straight, np.array([0, 0, -1]))
        diag1 = np.array([1, 1])
        diag2 = np.array([-1, 1])
        diag3 = np.array([1, -1])
        diag4 = np.array([-1, -1])
        arr = [straight, backwards, right, left, diag1, diag2, diag3, diag4]
        inputs = np.matrix([*[self.food_distance(x) for x in arr],
                            *[self.self_distance(x) for x in arr],
                            self.wall_distance(straight), self.wall_distance(backwards),
                            self.wall_distance(right), self.wall_distance(left)]).T
        # print(inputs)
        output = softmax(self.output(inputs/self.game.player.speed))
        # print("step:", output)
        moves = {0: straight[0:2], 1: right[0:2], 2: left[0:2]}

        return moves[np.argmax(output)]

    def food_distance(self, direction):
        direction = direction[0:2]
        curr_pos = np.array([self.game.player.x[0], self.game.player.y[0]])
        diff = np.array([*self.game.food])-curr_pos
        if np.array_equal(direction/np.linalg.norm(direction), diff/np.linalg.norm(diff)):
            return np.linalg.norm(diff)
        return 0

    def self_distance(self, direction):
        direction = direction[0:2]
        curr_pos = np.array([self.game.player.x[0], self.game.player.y[0]]) + self.game.player.speed * direction
        distance = 0

        while 80 <= curr_pos[0] <= 720 and 60 <= curr_pos[1] <= 540:
            if (curr_pos[0], curr_pos[1]) in list(zip(self.game.player.x, self.game.player.y)):
                return distance
            distance += self.game.player.speed
            curr_pos += self.game.player.speed * direction

        return 0

    def wall_distance(self, direction):
        # TODO maybe a better way to do this
        direction = direction[0:2]
        if np.array_equal(direction, [1, 0]):
            return 720-self.game.player.x[0]
        if np.array_equal(direction, [-1, 0]):
            return self.game.player.x[0]-80
        if np.array_equal(direction, [0, 1]):
            return self.game.player.y[0]-60
        if np.array_equal(direction, [0, -1]):
            return 540-self.game.player.y[0]


def sigmoid(z):
    """The sigmoid function."""
    return 1.0 / (1.0 + np.exp(-z))


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
