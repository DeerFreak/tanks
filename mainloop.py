import pygame as pg
import sys
import time as t
from pygame.locals import *
import numpy as np
from stats import *
from tank_class import Tank
from os import path
from spritesheet import Spritesheet
from sprites import *
from wall_class import *

class App(object):
    def __init__(self, surf):
        self.surf = surf
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.clock = pg.time.Clock()
        self.event_dict = {"w": False, "a": False, "s": False, "d": False, " ": False,\
                           "đ": False, "ē": False, "Ē": False, "Ĕ": False, "p": False,\
                           "c": False, "o": False}
        self.keys = pg.key.get_pressed()
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, "img")
        self.snd_dir = path.join(self.dir, "snd")
        self.expl1 = Spritesheet(path.join(self.img_dir, EXPL1))
        self.expl_dir = {"normal":[]}
        for row in range(8):
            for column in range(8):
                self.expl_dir["normal"].append(self.expl1.get_image(23 +column * 129, 40 + row * 128, 80, 90))

        game_icon = pg.image.load(path.join(self.img_dir, 'icon.png'))
        pg.display.set_icon(game_icon)

    def start(self):
        self.all_sprites = pg.sprite.Group()
        self.tanks = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.tank1 = Tank(self, "red")
        self.tank2 = Tank(self, "blue")
        self.tank2_group = pg.sprite.Group()
        self.tank2_group.add(self.tank2)
        for wall in WALLS:
            Wall(self, *wall)
        self.event_keys = {"c": self.tank1.next_weapon,
                           "o": self.tank2.next_weapon,
                           "č": pg.quit}  # Quit on "-" num block
        pg.mixer.music.load(path.join(self.snd_dir, "battle_march.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(MUSIC_VOL_INGAME)

        while self.tank1.health > 0 and self.tank2.health > 0:
            self.clock.tick(FPS)
            self.events()
            self.tank_update(+1)
            self.all_sprites.update()
            # collision of tanks
            if pg.sprite.spritecollide(self.tank1, self.tank2_group, False, pg.sprite.collide_mask):
                self.tank_update(-1)
                self.tanks.update()
            # collision of tanks & walls
            collisions = pg.sprite.groupcollide(self.tanks, self.walls, False, pg.sprite.collide_mask)
            #for col in collisions:
             #   col.tank_update(-1)
              #  self.tanks.update()

            self.bullets.update()
            self.check_bullet_hit()
            self.plot()

         # when signle game is finished
        while len(self.explosions) > 0:
            self.clock.tick(FPS)
            self.explosions.update()
            self.plot()
        pg.mixer.music.fadeout(500)


    def events(self):
        # Panzer1: WASD und Space
        # Panzer2: Pfeiltasten und P
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

    def tank_update(self, sign):
        self.tank1.moving = 0
        self.tank2.moving = 0
        if self.keys[pg.K_w]:
            self.tank1.moving = 1 * sign
        elif self.keys[pg.K_s]:
            self.tank1.moving = -1 * sign
        elif self.keys[pg.K_w] is False and self.keys[pg.K_s] is False:
            self.tank1.moving = 0
        if self.keys[pg.K_a]:
            self.tank1.calc_angle(-1 * sign)
        if self.keys[pg.K_d]:
            self.tank1.calc_angle(+1 * sign)
        if self.keys[pg.K_v] and sign == 1:
            reload_time = BULLETS[self.tank1.loaded_weapons[self.tank1.current_weapon]]["reload_time"]
            now = pg.time.get_ticks()
            if now - self.tank1.last_fired >= reload_time:
                self.tank1.fire()
                self.tank1.last_fired = now
        if self.keys[pg.K_UP]:
            self.tank2.moving = 1 * sign
        elif self.keys[pg.K_DOWN]:
            self.tank2.moving = -1 * sign
        elif self.keys[pg.K_UP] is False and self.keys[pg.K_DOWN] is False:
            self.tank2.moving = 0
        if self.keys[pg.K_LEFT]:
            self.tank2.calc_angle(-1 * sign)
        if self.keys[pg.K_RIGHT]:
            self.tank2.calc_angle(+1 * sign)
        if self.keys[pg.K_p] and sign == 1:
            reload_time = BULLETS[self.tank2.loaded_weapons[self.tank2.current_weapon]]["reload_time"]
            now = pg.time.get_ticks()
            if now - self.tank2.last_fired >= reload_time:
                self.tank2.fire()
                self.tank2.last_fired = now


    def check_bullet_hit(self):
        hits = pg.sprite.groupcollide(self.tanks, self.bullets, False, False)
        for hit in hits:
            if hit != hits[hit][0].shooter:
                hit.health -= hits[hit][0].dmg
                Explosion(self, hits[hit][0].rect.center, "normal", self.expl_dir)
                hits[hit][0].kill()

    def plot(self):
        self.surf.fill(BG_COLOR)
        self.draw_text(f"Player 1: {str(self.tank1.health)}HP", 30, RED, 120, 5)
        self.draw_text(f"Player 2: {str(self.tank2.health)}HP", 30, BLUE, 120, 35)
        # Game Loop - draw
        self.all_sprites.draw(self.surf)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.midtop = (x, y)
        self.surf.blit(text_surf, text_rect)

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "ls_music.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(MUSIC_VOL_LS)
        self.surf.fill(BG_COLOR)
        self.draw_text(NAME, 50, BLUE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("controls1: wasd c v", 22, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("controls2: Arrows o p", 22, BLUE, WIDTH / 2, HEIGHT / 2 + 25)
        self.draw_text("Press any key to play", 22, BLUE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "ls_music.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(1.2)
        self.surf.fill(BG_COLOR)
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