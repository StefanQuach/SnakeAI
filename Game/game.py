import pygame
import sys as system
from pygame import *
from Game.player import Player
import random
import numpy as np
import queue
from itertools import count
from AI.AI_Player import AIPlayer

win_width = 800
win_height = 600
low_bound = (80, 60)
up_bound = (720, 540)

RIGHT = np.array([1, 0])
LEFT = np.array([-1, 0])
UP = np.array([0, -1])
DOWN = np.array([0, 1])

moves = {K_UP: UP, K_DOWN: DOWN, K_RIGHT: RIGHT, K_LEFT: LEFT}
tiebreaker = count()


class Game:
    """
    Game object that runs the entirety of Snake, including Food placement.
    TODO: make a start screen and death screen
    """
    def __init__(self, fps=10, ai=False, caption='Snake'):
        """
        Constructor
        :param fps: in-game clock tick rate (in ticks/sec)
        """
        self._running = False
        self._display_surf = None
        self._player_surf = None
        self._food_surf = None
        self.fps = fps
        self.player = Player()
        self.food = (20*random.randint(low_bound[0]/20, up_bound[1]/20-1),  # initially spawning food
                     20*random.randint(low_bound[1]/20, up_bound[1]/20-1))
        self.score = 0
        self.ai = ai
        if ai:
            self.ai_player = AIPlayer(self, [5, 4], random=True)

        pygame.init()
        self.clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode((win_width, win_height), pygame.HWSURFACE)
        self._running = True
        self._player_surf = pygame.image.load("player.png").convert()
        self._food_surf = pygame.image.load("food.png").convert()
        self.buffer = queue.PriorityQueue(maxsize=2)
        self.caption = caption

    def render(self):
        """
        Helper method to store all the pygame rendering objects/processes
        :return:
        """
        pygame.display.set_caption(self.caption)
        self._display_surf.fill((0, 0, 0))
        rect = pygame.Rect(low_bound[0], low_bound[1],
                           up_bound[0]-low_bound[0], up_bound[1]-low_bound[1])
        pygame.draw.rect(self._display_surf, (255, 255, 255), rect, 1)
        self.player.draw(self._display_surf, self._player_surf)
        self._display_surf.blit(self._food_surf, self.food)
        my_font = pygame.font.SysFont("monospace", 16)
        score_text = my_font.render("Score = " + str(self.score), 1, (255, 255, 255))
        self._display_surf.blit(score_text, (5, 10))

        pygame.display.flip()
        pygame.display.update()

    def respawn_food(self):
        """
        Helper method to respawn the food in a valid place
        :return:
        """
        valid = False
        while not valid:
            x = 20*random.randint(low_bound[0]/20, up_bound[0]/20-1)
            y = 20*random.randint(low_bound[1]/20, up_bound[1]/20-1)
            valid = (x not in self.player.x) or (y not in self.player.y)
        self.food = (x, y)

    def check_eaten(self):
        """
        Checks if player has eaten the food, respawning food if the player has
        :return: True if food is eaten, else False
        """
        if (self.food[0] == self.player.x[0]) and (self.food[1] == self.player.y[0]):
            self.respawn_food()
            self.score += 1
            return True
        else:
            return False

    def check_death(self):
        """
        Checks if the player has died
        :return: True if the player has satisfied any death condition, else False
        """
        if (self.player.x[0], self.player.y[0]) in list(zip(self.player.x[1:], self.player.y[1:])):
            print('death by self')
            return True
        elif self.player.x[0] < low_bound[0] or self.player.x[0] > up_bound[0]-20:
            print('death by x-wall')
            return True
        elif self.player.y[0] < low_bound[1] or self.player.y[0] > up_bound[1]-20:
            print('death by y-wall')
            return True
        else:
            return False

    def valid_move(self, move):
        """
        Checks if the inputted move will actually do something
        :param move: input move
        :return: True if valid, False otherwise
        """
        if np.array_equal(-1*move, self.player.direction) or np.array_equal(move, self.player.direction):
            return 1
        else:
            return 0

    def run(self):
        self._running = True
        while self._running:
            if self.ai:
                self.player.change_direction(self.ai_player.next_move())
            else:
                key_events = pygame.event.get(KEYDOWN)
                # print(len(key_events))
                for ev in key_events:
                    if ev.key in moves:
                        if not self.buffer.full():
                            self.buffer.put((self.valid_move(moves[ev.key]), next(tiebreaker),
                                             moves[ev.key]), block=False)
                        else:
                            print('full')

                    if ev.key is K_ESCAPE:
                        # exit the game if esc is pressed
                        pygame.quit()
                        system.exit()

                # print(self.buffer.qsize())
                if not self.buffer.empty():  # take the moves one at a time, dequeuing one per frame
                    x = self.buffer.get(block=False)[2]
                    # print('Moving', x)
                    self.player.change_direction(x)

            eat = self.check_eaten()
            self.player.move(eat)
            self._running = not self.check_death()

            self.render()
            self.clock.tick(self.fps)

        pygame.quit()
        system.exit()


if __name__ == "__main__":
    game = Game(fps=10, ai=True)
    game.run()
