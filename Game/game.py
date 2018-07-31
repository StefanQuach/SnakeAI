import pygame
from pygame import *
from player import Player
import random
import numpy as np

win_width = 800
win_height = 600
low_bound = (80, 60)
up_bound = (720, 540)

RIGHT = np.array([1, 0])
LEFT = np.array([-1, 0])
UP = np.array([0, -1])
DOWN = np.array([0, 1])

moves = {K_UP: UP, K_DOWN: DOWN, K_RIGHT: RIGHT, K_LEFT: LEFT}

class Game:
    
    def __init__(self, fps=10):
        self._running = False
        self._display_surf = None
        self._player_surf = None
        self._food_surf = None
        self.fps = fps
        self.player = Player()
        self.food = (20*random.randint(low_bound[0]/20, up_bound[1]/20-1),
                     20*random.randint(low_bound[1]/20, up_bound[1]/20-1))
        self.score = 0
        pygame.init()
        self.clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode((win_width, win_height), pygame.HWSURFACE)
        self._running = True
        self._player_surf = pygame.image.load("player.png").convert()
        self._food_surf = pygame.image.load("food.png").convert()

    def on_render(self):
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
        valid = False
        while not valid:
            x = 20*random.randint(low_bound[0]/20, up_bound[0]/20-1)
            y = 20*random.randint(low_bound[1]/20, up_bound[1]/20-1)
            valid = (x not in self.player.x) or (y not in self.player.y)
        self.food = (x, y)

    def check_eaten(self):
        if (self.food[0] == self.player.x[0]) and (self.food[1] == self.player.y[0]):
            self.respawn_food()
            self.score += 1
            return True
        else:
            return False

    def check_death(self):
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

    def run(self):
        self._running = True
        while self._running:
            key_events = pygame.event.get(KEYDOWN)  # TODO implement a Queue to keep a buffer of moves?
            if len(key_events) <= 1:
                for ev in key_events:
                    if ev.key in moves:
                        self.player.change_direction(moves[ev.key])
                    elif ev.key is K_ESCAPE:  # TODO fix exit method
                        self._running = False

            eat = self.check_eaten()
            self.player.move(eat)
            self._running = not self.check_death()

            self.on_render()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game()
    game.run()
