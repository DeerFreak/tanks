import pygame
import math as m
import numpy as np
from colors import *
from stats import turn_speed, tank_speed, tank_gear, resolution
from bullet_class import Bullet


class Tank(pygame.sprite.Sprite):
    def __init__(self, start_pos, surf, color):
        pygame.sprite.Sprite.__init__(self)
        if color == "red":  # tank1
            img = "tank_red.png"
        else:  # tank2
            img = "tank_blue.png"
        self.image = pygame.image.load(img).convert_alpha()  # plot
        self.alive = True  # tank alive

        self.turn_speed = -turn_speed  # tank position_stats
        self.speed = tank_speed
        self.moving = 0
        
        self.loaded_weapons = ["normal", "berta"]
        self.current_weapon = 0
        
        self.angle = 0
        self.pos = [start_pos[0], start_pos[1]]
        
        self.rect = self.image.get_rect()  # Plot-details
        self.surf = surf
        self.toRotate = self.image.copy()  # plot

    def move(self):
        pos_old = self.pos[:]  # to reset if outside of borders
        self.pos[0] += (m.cos(m.radians(self.angle)) * tank_gear[self.moving]) # x-pos
        self.pos[1] -= (m.sin(m.radians(self.angle)) * tank_gear[self.moving]) # y-pos
        self.calc_rect()
        self.pos_border_check(pos_old)

    def fire(self):
        bullet = Bullet(self.pos, self.angle, self.loaded_weapons[self.current_weapon], self, self.surf)
        return bullet

    def next_weapon(self):
        self.current_weapon = (self.current_weapon + 1) % len(self.loaded_weapons)

    def pos_border_check(self, pos_old):
        if self.rect[0] < 0 or self.rect[0] + self.rect[2] > resolution[0]:  # x-borders
            self.pos[0] = pos_old[0]  # if outside

        if self.rect[1] < 0 or self.rect[1] + self.rect[3] > resolution[1]:  # y-borders
            self.pos[1] = pos_old[1]  # if outside
    
    def angle_border_check(self, dir):
        if self.rect[0] < 0 or self.rect[0] + self.rect[2] > resolution[0]:  # angle change would place tank outside
            self.angle -= self.turn_speed * dir
            self.calc_rect()  # to get right plot
        if self.rect[1] < 0 or self.rect[1] + self.rect[3] > resolution[1]:  # angle change would place tank outside
            self.angle -= self.turn_speed * dir
            self.calc_rect()  # to get right plot

    def plot(self):
        # calc_rect # only if not calced before
        self.surf.blit(self.toRotate, self.rect)  # rest is already calced

    def calc_angle(self, dir):
        self.angle += self.turn_speed * dir  # turn
        self.calc_rect()  # new tank pos
        self.angle_border_check(dir)  # checking for borders and if so reset

    def calc_rect(self):
        self.toRotate = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.toRotate.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
