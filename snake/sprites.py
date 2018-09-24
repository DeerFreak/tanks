import pygame as pg
import time as t
from colors import colors
from settings import *

class Snake(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.group_snake
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.screen = game.screen
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(colors["red1"])
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = (0, 0)


class Apple(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.snake
        pg.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        pass