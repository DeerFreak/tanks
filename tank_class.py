import pygame as pg
import math as m
import numpy as np
from stats import *
from bullet_class import Bullet

vec = pg.math.Vector2


class Tank(pg.sprite.Sprite):
    def __init__(self, game, color):
        self._layer = TANK_LAYER
        self.groups = game.all_sprites, game.tanks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.angle = 0
        self.color = color
        self.pos = vec(TANK_START_POS[self.color])

        self.surf = game.surf
        img = {"red":"tank_red_2.png","blue":"tank_blue_2.png"}
        self.image_org = pg.image.load(img[self.color]).convert()
        self.image_org.set_colorkey(WHITE)
        self.image = self.image_org.copy()
        self.image.set_colorkey(WHITE)  # plot
        self.rect = self.image.get_rect(center=self.pos)  # Plot-details
        self.mask = pg.mask.from_surface(self.image)

        self.alive = True  # tank alive
        self.health = 200

        self.turn_speed = -turn_speed  # tank position_stats
        self.speed = tank_speed
        self.moving = 0
        
        self.loaded_weapons = ["normal", "berta"]
        self.current_weapon = 0
        

        
    def update(self):
        self.move()


    def move(self):
        pos_old = self.pos[:]  # to reset if outside of borders
        self.pos.x += (m.cos(m.radians(self.angle)) * tank_gear[self.moving]) # x-pos
        self.pos.y -= (m.sin(m.radians(self.angle)) * tank_gear[self.moving]) # y-pos
        self.calc_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.pos_border_check(pos_old)

    def fire(self):
        Bullet(self)

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

    def calc_angle(self, dir):
        self.angle += self.turn_speed * dir  # turn
        self.calc_rect()  # new tank pos
        self.angle_border_check(dir)  # checking for borders and if so reset

    def calc_rect(self):
        self.image = pg.transform.rotate(self.image_org, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

