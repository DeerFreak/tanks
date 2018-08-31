import pygame as pg
import time as t
from pygame.locals import *
import numpy as np
import random
from sprites import *
from wall_class import *
from stats import *
from tank_class import Tank
from os import path
from spritesheet import Spritesheet
from init import load_App_data
from tiled_map import TiledMap

def draw_tank_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class App(object):
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.clock = pg.time.Clock()
        self.event_dict = {"w": False, "a": False, "s": False, "d": False, " ": False,\
                           "đ": False, "ē": False, "Ē": False, "Ĕ": False, "p": False,\
                           "c": False, "o": False}
        self.keys = pg.key.get_pressed()
        load_App_data(self)

    def new(self):
        # all sprite groups
        self.all_sprites = pg.sprite.Group()
        self.tanks = pg.sprite.Group()
        self.tank2_group = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        # load map
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'tank1':
                self.tank1 = Tank(self, "red", tile_object.x, tile_object.y)
            if tile_object.name == 'tank2':
                self.tank2 = Tank(self, "blue", tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                 tile_object.width, tile_object.height)
        # rest
        self.tank2_group.add(self.tank2)
        self.event_keys = {"c": self.tank1.next_weapon,
                           "o": self.tank2.next_weapon,
                           "č": pg.quit}  # Quit on "-" num block
        # start game music
        pg.mixer.music.load(path.join(self.snd_dir, "battle_march.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(MUSIC_VOL_INGAME)

    def start(self):
        self.new()
        while self.tank1.health > 0 and self.tank2.health > 0:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.all_sprites.update()
            self.bullets.update()
            self.collisions()
            self.draw()


    def collisions(self):
        # collision of tanks
        (self.tank1.sign, self.tank2.sign) = (-1,) * 2  # for all tank collisions
        if pg.sprite.spritecollide(self.tank1, self.tank2_group, False):  # to improve performance
            if pg.sprite.spritecollide(self.tank1, self.tank2_group, False, pg.sprite.collide_mask):
                self.tanks.update()
        # collision of tanks & walls # NEEDS FIX - BUG - shift to tank_class.py
        if pg.sprite.groupcollide(self.tanks, self.walls, False, False, pg.sprite.collide_mask): # to improve performance
            collisions = pg.sprite.groupcollide(self.tanks, self.walls, False, False, pg.sprite.collide_mask)
            for col in collisions:
                col.update()
        (self.tank1.sign, self.tank2.sign) = (1,) * 2  # reset sign after tank collisions

    def events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.running = False
                pg.quit()
            if event.type == KEYDOWN:
                try:
                    self.event_keys[chr(event.key)]()
                except:
                    pass
        self.keys = pg.key.get_pressed()

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) # FPS TITLE
        self.screen.blit(self.map_img, self.map_rect)
        self.draw_text("Player 1:", 30, RED, 150, 15)
        self.draw_text("Player 2:", 30, BLUE, 700, 15)
        draw_tank_health(self.screen, 210, 20, self.tank1.health / TANK_HEALTH)
        draw_tank_health(self.screen, 760, 20, self.tank2.health / TANK_HEALTH)
        # Game Loop - draw
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_screen = font.render(text, True, color)
        text_rect = text_screen.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_screen, text_rect)

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "ls_music.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(MUSIC_VOL_LS)
        self.screen.fill(BG_COLOR)
        self.draw_text(NAME, 50, BLUE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("controls1: wasd c v", 22, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("controls2: Arrows o p", 22, BLUE, WIDTH / 2, HEIGHT / 2 + 25)
        self.draw_text("Press any key to play", 22, BLUE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # to not cut explosion in the end
        while len(self.explosions) > 0:
            self.clock.tick(FPS)
            self.explosions.update()
            self.draw()
        pg.mixer.music.fadeout(500)
        # begin "real" go-screen
        pg.mixer.music.load(path.join(self.snd_dir, "ls_music.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(1.2)
        self.screen.fill(BG_COLOR)
        if self.tank1.health > 0:
            win_text = "Player 1 won!"
        else:
            win_text = "Player 2 won!"
        self.draw_text(f"{win_text}", 22, BLUE, WIDTH / 2, 10)
        self.draw_text("", 50, BLUE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f"", 22, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 22, BLUE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        if not self.running:
            return
        for sprite in self.all_sprites: # if one of them dies to clear space for new game
            sprite.kill()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False