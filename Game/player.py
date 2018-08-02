import numpy as np


class Player:
    def __init__(self, x=100, y=60, speed=20):
        # creating the main body initially length 3
        self.x = []
        self.y = []
        self.x.extend([x, x-1*speed, x-2*speed])
        self.y.extend([y, y, y])
        # initializing movement variables
        self.speed = speed
        self.direction = np.array([1, 0])

    def change_direction(self, direction):
        if not np.array_equal(-1*direction, self.direction):
            self.direction = direction

    def move(self, elongate):
        # if elongation is necessary
        if elongate:
            self.x.append(self.x[-1])
            self.y.append(self.y[-1])

        # moving the rest of the body
        for i in reversed(range(1, len(self.x))):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # moving the head
        new = np.array([self.x[0], self.y[0]]) + np.array(self.direction)*self.speed
        self.x[0] = new[0]
        self.y[0] = new[1]

    def draw(self, surface, image):
        for i in range(0, len(self.x)):
            surface.blit(image, (self.x[i], self.y[i]))
