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
        
        if color == "red":
            img = "tank_red.png"
        else:
            img = "tank_blue.png"
        self.cross = pygame.image.load(img).convert_alpha()
        self.toRotate = self.cross.copy()

    def move(self):
        self.pos[0] += (m.cos(m.radians(self.angle)) * self.gear[self.moving])
        self.pos[1] += (-m.sin(m.radians(self.angle)) * self.gear[self.moving])
        print(self.pos)

    def plot(self):
        self.toRotate = pygame.transform.rotate(self.cross, self.angle)
        rect = self.toRotate.get_rect(center=(int(self.pos[0]),int(self.pos[1])))
        self.surf.blit(self.toRotate,rect)

