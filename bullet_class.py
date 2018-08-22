import time as t
from stats import bullets
import pygame
from colors import *
import math as m


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos0, angle0, type, shooter, surf):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos0[:]
        self.angle = angle0
        self.type = type
        self.speed = bullets[type]["vel"]
        self.shooter = shooter
        self.t_expire = t.time() + bullets[type]["l_time"]

        self.surf = surf

    def move(self):
        self.pos[0] += (m.cos(m.radians(self.angle)) * self.speed)  # x-pos
        self.pos[1] -= (m.sin(m.radians(self.angle)) * self.speed)  # y-pos

    def time_check(self):
        pass

    def pos_time_check(self):
        pass

    def plot(self):
        pos = [None] * 2
        pos[0] = int(self.pos[0])
        pos[1] = int(self.pos[1])
        pygame.draw.circle(self.surf, bullets[self.type]["color"], pos, bullets[self.type]["size"])
