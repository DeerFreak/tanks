import pygame as pg
from stats import *
from os import path
from random import choice

vec = pg.math.Vector2

# image only here for collisions 

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        val = [int(i) for i in [x, y, w, h]]
        self.image = pg.Surface((val[2], val[3])).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
