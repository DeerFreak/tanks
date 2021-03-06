import pygame as pg
from stats import *

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, center, explosion_anim):
        self._layer = EXPLOSION_LAYER
        self.groups = game.all_sprites, game.explosions
        pg.sprite.Sprite.__init__(self, self.groups)
        self.expl_anim = explosion_anim
        self.image = self.expl_anim[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = FRAME_TICK_RATES_EXPL
        game.expl_snd_dir["normal"].play()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.expl_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.expl_anim[self.frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = center

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE