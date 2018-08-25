import pygame as pg
from stats import *
from os import path
from random import choice
scales = [(100, 10),(234, 24),(28, 97),(230, 23)]

class Wall(pg.sprite.Sprite):
    def __init__(self, game, pos0, angle0):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites # walls not beeing added for spawning
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos0[:]
        self.angle = angle0
        self.image = pg.image.load(path.join(game.img_dir, "wall.png")).convert()
        self.image.set_colorkey(WHITE)
        self.image = pg.transform.scale(self.image, choice(scales))
        self.image = pg.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center = self.pos)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        pass
