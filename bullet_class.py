import time as t
from stats import *
import pygame as pg
import math as m
from os import path
vec = pg.math.Vector2

class Bullet(pg.sprite.Sprite):
    def __init__(self, shooter):
        game = shooter.game
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.shooter = shooter
        self.pos = self.shooter.pos[:]
        self.angle = shooter.angle
        self.type = shooter.loaded_weapons[shooter.current_weapon]
        self.image = game.img_bullets[self.type][self.shooter.color].copy() # get copy of bullet img
        self.image = pg.transform.rotate(self.image, self.angle) # rotate to appropiate angle
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.speed = BULLETS[self.type]["vel"]
        self.dmg = BULLETS[self.type]["dmg"]
        self.game.shot_snd_dir[self.type].play() # play sound when created
        self.expire_time = pg.time.get_ticks() + BULLETS[self.type]["l_time"]
        self.surf = game.surf

    def update(self):
        self.time_check()
        self.pos[0] += (m.cos(m.radians(self.angle)) * self.speed)  # x-pos
        self.pos[1] -= (m.sin(m.radians(self.angle)) * self.speed)  # y-pos
        self.rect = self.image.get_rect(center=(int(self.pos[0]), int(self.pos[1])))

    def time_check(self):
        if pg.time.get_ticks() >= self.expire_time:
            self.kill()