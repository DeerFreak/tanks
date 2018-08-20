import pygame
import math as m
import numpy as np
from colors import *


class Tank(object):
    def __init__(self, start_pos, surf, color):
        self.alive = True # tank alive

        self.turn_speed = -0.15 # tank position_stats
        self.speed = 0.3
        self.moving = 0
        self.gear = {0:0, 1:self.speed, -1:-self.speed}
        self.angle = 0
        self.pos = [start_pos[0], start_pos[1]]
        
        self.rect = None # Plot-details
        self.surf = surf 
        if color == "red": # tank1
            img = "tank_red.png"
        else: # tank2
            img = "tank_blue.png"
        self.cross = pygame.image.load(img).convert_alpha() # plot
        self.toRotate = self.cross.copy() # plot

    def move(self):
        pos_old = self.pos[:] # to reset if outside of borders
        self.pos[0] += (m.cos(m.radians(self.angle)) * self.gear[self.moving]) # x-pos
        self.pos[1] -= (m.sin(m.radians(self.angle)) * self.gear[self.moving]) # y-pos
        self.calc_rect()
        self.pos_border_check()

    def pos_border_check(self):
        if self.rect[0] < 0 or self.rect[0] + self.rect[2] > 1000: # x-borders
            self.pos[0] = pos_old[0] # if outside

        if self.rect[1] < 0 or self.rect[1] + self.rect[3] > 1000: # y-borders
            self.pos[1] = pos_old[1] # if outside
    
    def angle_border_check(self):
        if self.rect[0] < 0 or self.rect[0] + self.rect[2] > 1000: # angle change would place tank outside
            self.angle -= self.turn_speed * dir
            self.calc_rect() # to get right plot
        if self.rect[1] < 0 or self.rect[1] + self.rect[3] > 1000: # angle change would place tank outside
            self.angle -= self.turn_speed * dir
            self.calc_rect() # to get right plot

    def plot(self):
        # calc_rect # only if not calced before
        self.surf.blit(self.toRotate,self.rect) # rest is already calced

    def calc_angle(self, dir):
        self.angle += self.turn_speed * dir # turn
        self.calc_rect() # new tank pos
        self.angle_border_check() # checking for borders and if so reset

    def calc_rect(self):
        self.toRotate = pygame.transform.rotate(self.cross, self.angle)
        self.rect = self.toRotate.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
