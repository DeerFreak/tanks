import pygame as pg
import math as m
import numpy as np
from stats import *
from bullet_class import Bullet
from os import path

vec = pg.math.Vector2

class Tank(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        self._layer = TANK_LAYER
        self.groups = game.all_sprites, game.tanks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.angle = 0
        self.color = color
        self.pos = vec(x, y)
        self.last_fired = 0
        self.sign = 1

        self.screen = game.screen
        self.image_org = game.img_tanks[self.color]
        self.image = self.image_org.copy()
        self.image.set_colorkey(WHITE)  # plot
        self.rect = self.image.get_rect(center=self.pos)  # Plot-details
        self.mask = pg.mask.from_surface(self.image)

        self.alive = True  # tank alive
        self.health = TANK_HEALTH

        self.turn_speed = -TURN_SPEED  # tank position_stats
        self.speed = TANK_SPEED
        self.moving = 0
        
        self.loaded_weapons = ["normal", "berta"]
        self.current_weapon = 0

    def update(self):
        self.moving = 0
        if self.color == "red":
            if self.game.keys[pg.K_w]:
                self.moving = 1 * self.sign
            elif self.game.keys[pg.K_s]:
                self.moving = -1 * self.sign
            elif self.game.keys[pg.K_w] is False and self.game.keys[pg.K_s] is False:
                self.moving = 0
            if self.game.keys[pg.K_a]:
                self.calc_angle(-1 * self.sign)
            if self.game.keys[pg.K_d]:
                self.calc_angle(+1 * self.sign)
            if self.game.keys[pg.K_v] and self.sign == 1:
                reload_time = BULLETS[self.loaded_weapons[self.current_weapon]]["reload_time"]
                now = pg.time.get_ticks()
                if now - self.last_fired >= reload_time:
                    self.fire()
                    self.last_fired = now
        else:
            if self.game.keys[pg.K_UP]:
                self.moving = 1 * self.sign
            elif self.game.keys[pg.K_DOWN]:
                self.moving = -1 * self.sign
            elif self.game.keys[pg.K_UP] is False and self.game.keys[pg.K_DOWN] is False:
                self.moving = 0
            if self.game.keys[pg.K_LEFT]:
                self.calc_angle(-1 * self.sign)
            if self.game.keys[pg.K_RIGHT]:
                self.calc_angle(+1 * self.sign)
            if self.game.keys[pg.K_p] and self.sign == 1:
                reload_time = BULLETS[self.loaded_weapons[self.current_weapon]]["reload_time"]
                now = pg.time.get_ticks()
                if now - self.last_fired >= reload_time:
                    self.fire()
                    self.last_fired = now
        self.move()

    def move(self):
        pos_old = vec(self.pos)  # to reset if outside of borders
        self.pos.x += (m.cos(m.radians(self.angle)) * TANK_GEAR[self.moving] * self.game.dt) # x-pos
        self.pos.y -= (m.sin(m.radians(self.angle)) * TANK_GEAR[self.moving] * self.game.dt) # y-pos
        self.calc_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.pos_border_check(pos_old)

    def fire(self):
        Bullet(self, self.game)

    def next_weapon(self):
        self.current_weapon = (self.current_weapon + 1) % len(self.loaded_weapons)

    def pos_border_check(self, pos_old):
        if self.rect.left < 0 or self.rect.right > RESOLUTION[0]:  # x-borders
            self.pos.x = pos_old.x  # if outside

        if self.rect.top < 0 or self.rect.bottom > RESOLUTION[1]:  # y-borders
            self.pos.y = pos_old.y  # if outside
    
    def angle_border_check(self, dir):
        if self.rect[0] < 0 or self.rect[0] + self.rect[2] > RESOLUTION[0]:  # angle change would place tank outside
            self.angle -= self.turn_speed * dir * self.game.dt
            self.calc_rect()  # to get right plot
        if self.rect[1] < 0 or self.rect[1] + self.rect[3] > RESOLUTION[1]:  # angle change would place tank outside
            self.angle -= self.turn_speed * dir * self.game.dt
            self.calc_rect()  # to get right plot

    def calc_angle(self, dir):
        self.angle += self.turn_speed * dir * self.game.dt # turn
        self.calc_rect()  # new tank pos
        self.angle_border_check(dir)  # checking for borders and if so reset

    def calc_rect(self):
        self.image = pg.transform.rotate(self.image_org, self.angle)
        self.rect = self.image.get_rect(center=self.pos)