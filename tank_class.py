import pygame
import math as m
import numpy as np
from colors import *


class Tank(object):
    def __init__(self, start_pos, surf, color):
        self.surf = surf
        self.alive = True

        self.turn_speed = -0.15
        self.speed = 0.3
        self.moving = 0
        self.gear = {0:0, 1:self.speed, -1:-self.speed}
        self.angle = 0
        self.pos = [start_pos[0], start_pos[1]]
        self.rect = None
        
        if color == "red":
            img = "tank_red.png"
        else:
            img = "tank_blue.png"
        self.cross = pygame.image.load(img).convert_alpha()
        self.toRotate = self.cross.copy()

    def move(self):
        pos_old = self.pos[:]
        self.pos[0] += (m.cos(m.radians(self.angle)) * self.gear[self.moving])
        self.pos[1] += (-m.sin(m.radians(self.angle)) * self.gear[self.moving])
        self.calc_rect()
        if self.rect[0] < 0 or self.rect[0] + self.rect[2] > 1000:
            self.pos[0] = pos_old[0]

        if self.rect[1] < 0 or self.rect[1] + self.rect[3] > 1000:
            self.pos[1] = pos_old[1]


    def plot(self):
        self.surf.blit(self.toRotate,self.rect)

    def calc_angle(self, dir):
        self.angle += self.turn_speed * dir
        self.calc_rect()
        if self.rect[0] < 0 or self.rect[0] + self.rect[2] > 1000:
            self.angle -= self.turn_speed * dir
            self.calc_rect()
        if self.rect[1] < 0 or self.rect[1] + self.rect[3] > 1000:
            self.angle -= self.turn_speed * dir
            self.calc_rect()


    def calc_rect(self):
        self.toRotate = pygame.transform.rotate(self.cross, self.angle)
        self.rect = self.toRotate.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
