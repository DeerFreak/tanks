import pygame as pg
import sys
import time as t
from pygame.locals import *
import numpy as np
from stats import *
from tank_class import Tank


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

    def start(self):
        self.all_sprites = pg.sprite.Group()
        self.tanks = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.tank1 = Tank(self, "red")
        self.tank2 = Tank(self, "blue")
        self.tank2_group = pg.sprite.Group()
        self.tank2_group.add(self.tank2)
        self.event_keys = {"c": self.tank1.next_weapon,
                           "o": self.tank2.next_weapon,
                           "č": pg.quit}  # Quit on "-" num block
        self.last_fire = [0, 0]
        self.last_reload = [0, 0]

        while self.tank1.health > 0 and self.tank2.health > 0:
            self.clock.tick(FPS)
            self.events()
            self.tank_update(+1)
            self.all_sprites.update()
            if pg.sprite.spritecollide(self.tank1, self.tank2_group, False, pg.sprite.collide_mask):
                self.tank_update(-1)
                self.tanks.update()
            self.bullets.update()
            self.check_bullet_hit()
            self.plot()


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
            temp = BULLETS[self.tank1.loaded_weapons[self.tank1.current_weapon]]["reload_time"]
            if (t.time() - self.last_fire[0]) >= temp:
                self.tank1.fire()
                self.last_fire[0] = t.time()
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
            temp = BULLETS[self.tank2.loaded_weapons[self.tank2.current_weapon]]["reload_time"]
            if (t.time() - self.last_fire[1]) >= temp:
                self.tank2.fire()
                self.last_fire[1] = t.time()


    def check_bullet_hit(self):
        hits = pg.sprite.groupcollide(self.tanks, self.bullets, False, False)
        for hit in hits:
            if hit != hits[hit][0].shooter:
                hit.health -= hits[hit][0].dmg
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
        self.surf.fill(BG_COLOR)
        self.draw_text(NAME, 50, BLUE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("controls1: wasd c v", 22, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("controls2: Arrows o p", 22, BLUE, WIDTH / 2, HEIGHT / 2 + 25)
        self.draw_text("Press any key to play", 22, BLUE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
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