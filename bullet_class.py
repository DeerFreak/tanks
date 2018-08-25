import time as t
from stats import *
import pygame
import math as m


class Bullet(pygame.sprite.Sprite):
    def __init__(self, shooter):
        game = shooter.game
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = shooter.pos[:]
        self.angle = shooter.angle
        self.type = shooter.loaded_weapons[shooter.current_weapon]
        img = {"normal":pygame.image.load("bullet_normal.png").convert(), "berta":pygame.image.load("bullet_berta.png").convert()}
        self.image = img[self.type]
        self.rect = self.image.get_rect()
        self.speed = BULLETS[self.type]["vel"]
        self.dmg = BULLETS[self.type]["dmg"]
        self.shooter = shooter
        self.t_expire = t.time() + BULLETS[self.type]["l_time"]
        self.shoot_time = t.time()

        self.surf = game.surf

    def update(self):
        self.pos[0] += (m.cos(m.radians(self.angle)) * self.speed)  # x-pos
        self.pos[1] -= (m.sin(m.radians(self.angle)) * self.speed)  # y-pos
        self.rect = self.image.get_rect(center=(int(self.pos[0]), int(self.pos[1])))

    def time_check(self):
        pass

    def pos_time_check(self):
        pass
