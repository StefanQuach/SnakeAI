import pygame
from pygame import *
import time
from player import Player
import random


class Game:
    win_width = 800
    win_height = 600
    low_bound = (80, 60)
    up_bound = (720, 540)

    def __init__(self):
        self._running = False
        self._display_surf = None
        self._player_surf = None
        self._food_surf = None
        self.player = Player()
        self.food = (20*random.randint(self.low_bound[0]/20, self.up_bound[1]/20-1),
                     20*random.randint(self.low_bound[1]/20, self.up_bound[1]/20-1))
        self.score = 0

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.win_width, self.win_height), pygame.HWSURFACE)
        self._running = True
        self._player_surf = pygame.image.load("player.png").convert()
        self._food_surf = pygame.image.load("food.png").convert()

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        rect = pygame.Rect(self.low_bound[0], self.low_bound[1],
                           self.up_bound[0]-self.low_bound[0], self.up_bound[1]-self.low_bound[1])
        pygame.draw.rect(self._display_surf, (255, 255, 255), rect, 1)
        self.player.draw(self._display_surf, self._player_surf)
        self._display_surf.blit(self._food_surf, self.food)
        my_font = pygame.font.SysFont("monospace", 16)
        score_text = my_font.render("Score = " + str(self.score), 1, (255, 255, 255))
        self._display_surf.blit(score_text, (5, 10))

        pygame.display.flip()

    def respawn_food(self):
        valid = False
        while not valid:
            x = 20*random.randint(self.low_bound[0]/20, self.up_bound[0]/20-1)
            y = 20*random.randint(self.low_bound[1]/20, self.up_bound[1]/20-1)
            valid = (x in self.player.x) or (y in self.player.y)
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
            print(self.player.x, self.player.y)
            return True
        elif self.player.x[0] < self.low_bound[0] or self.player.x[0] > self.up_bound[0]-20:
            print('b')
            return True
        elif self.player.y[0] < self.low_bound[1] or self.player.y[0] > self.up_bound[1]-20:
            print('c')
            return True
        else:
            return False

    def run(self, delay):
        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.player.move_right()

            if keys[K_LEFT]:
                self.player.move_left()

            if keys[K_UP]:
                self.player.move_up()

            if keys[K_DOWN]:
                self.player.move_down()

            if keys[K_ESCAPE]:
                self._running = False

            eat = self.check_eaten()
            self.player.move(eat)
            if self.check_death():
                print('ded')
                self._running = False

            self.on_render()
            time.sleep(delay/1000.0)


if __name__ == "__main__":
    game = Game()
    game.run(100)
