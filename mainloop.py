import pygame as pg
import sys
import time as t
from pygame.locals import *
import numpy as np
from stats import *
from tank_class import Tank


class App(object):
    def __init__(self, surf, FPS):
        self.surf = surf
        self.all_sprites = pg.sprite.Group()
        self.tanks = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.tank1 = Tank(self, "red")
        self.tank2 = Tank(self, "blue")
        self.tank2_group = pg.sprite.Group()
        self.tank2_group.add(self.tank2)

        self.running = True
        self.delta_frame = 1 / FPS
        self.event_dict = {"w": False, "a": False, "s": False, "d": False, " ": False,
                           "đ": False, "ē": False, "Ē": False, "Ĕ": False, "p": False,
                           "c": False, "o": False}
        self.event_keys = {"c": self.tank1.next_weapon,
                           "o": self.tank2.next_weapon,
                           "č": pg.quit}  # Quit on "-" num block
        self.last_fire = [0, 0]
        self.last_reload = [0, 0]

    def start(self):
        pg.init()
        time = t.time()

        while self.running:
            if (t.time() - time) >= self.delta_frame:

                time = t.time()
                self.events() 
                self.tank_key_assignment() 
                self.tank_move()
                self.bullet_move()
                self.check_tank_collision()
                self.check_bullet_hit()

                self.plot()
                if self.tank1.health <= 0 or self.tank2.health <= 0:
                    self.running = False

        # Game is over
        if self.tank1.health <= 0:
            winner = "Spieler 2"
        else:
            winner = "Spieler 1"
        print("Der Gewinner ist " + winner + "!")
        t.sleep(0.5)
        self.surf.fill(WHITE)
        font = pg.font.SysFont("comicsansms", 50)
        text = font.render("Sieger: " + winner, True, (0, 128, 0))
        self.surf.blit(text, (resolution[0]/2 - text.get_width()/2,
                              resolution[1]/2 - text.get_height()/2))
        pg.display.update()
        t.sleep(3)

    def events(self):
        # Panzer1: WASD und Space
        # Panzer2: Pfeiltasten und P
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        
            if event.type == KEYDOWN:
                for key in self.event_keys:
                    if chr(event.key) == key:
                        print("True")
                        self.event_keys[key]()
                        return
                self.event_dict[chr(event.key)] = True

            if event.type == KEYUP:
                self.event_dict[chr(event.key)] = False

    def check_tank_collision(self):  # tank collision

        collision = pg.sprite.spritecollide(self.tank1, self.tank2_group, False, pg.sprite.collide_mask)
        if collision:
            if self.event_dict["w"]:
                self.tank1.moving = -1
            elif self.event_dict["s"]:
                self.tank1.moving = 1
            if self.event_dict["đ"]:
                self.tank2.moving = -1
            elif self.event_dict["Ē"]:
                self.tank2.moving = 1
            if self.event_dict["a"]:
                self.tank1.calc_angle(+1)
            if self.event_dict["d"]:
                self.tank1.calc_angle(-1)
            if self.event_dict["Ĕ"]:
                self.tank2.calc_angle(+1)
            if self.event_dict["ē"]:
                self.tank2.calc_angle(-1)

            self.tank1.move()
            self.tank2.move()

    def check_bullet_hit(self):
        hits = pg.sprite.groupcollide(self.tanks, self.bullets, False, False)
        for hit in hits:
            if hit != hits[hit][0].shooter:
                hit.health -= hits[hit][0].dmg
                hits[hit][0].kill()

    def tank_key_assignment(self):
        self.tank1_key_assignment()
        self.tank2_key_assignment()

    def tank1_key_assignment(self):
        if self.event_dict["w"]:
            self.tank1.moving = 1
        elif self.event_dict["s"]:
            self.tank1.moving = -1
        elif self.event_dict["w"] is False and self.event_dict["s"] is False:
            self.tank1.moving = 0
        if self.event_dict["a"]:
            self.tank1.calc_angle(-1)
        if self.event_dict["d"]:
            self.tank1.calc_angle(+1)
        if self.event_dict[" "]:
            temp = BULLETS[self.tank1.loaded_weapons[self.tank1.current_weapon]]["reload_time"]
            if (t.time() - self.last_fire[0]) >= temp:
                self.tank1.fire()
                self.last_fire[0] = t.time()

    def tank2_key_assignment(self):
        if self.event_dict["đ"]:
            self.tank2.moving = 1
        elif self.event_dict["Ē"]:
            self.tank2.moving = -1
        elif self.event_dict["đ"] is False and self.event_dict["Ē"] is False:
            self.tank2.moving = 0
        if self.event_dict["Ĕ"]:
            self.tank2.calc_angle(-1)
        if self.event_dict["ē"]:
            self.tank2.calc_angle(+1)
        if self.event_dict["p"]:
            temp = BULLETS[self.tank2.loaded_weapons[self.tank2.current_weapon]]["reload_time"]
            if (t.time() - self.last_fire[1]) >= temp:
                self.tank2.fire()
                self.last_fire[1] = t.time()

    def tank_move(self):
        self.tank1.move()
        self.tank2.move()
    
    def bullet_move(self):
        for bullet in self.bullets:
            bullet.move()

    def plot(self):
        self.surf.fill(WHITE)
        font = pg.font.SysFont("comicsansms", 20)
        text1 = font.render("Player 1: " + str(self.tank1.health) + " HP", True, (0, 128, 0))
        text2 = font.render("Player 2: " + str(self.tank2.health) + " HP", True, (0, 128, 0))
        self.surf.blit(text1, (0, 0))
        self.surf.blit(text2, (0, 30))
        # Game Loop - draw
        self.all_sprites.draw(self.surf)
        # *after* drawing everything, flip the display
        pg.display.flip()

        pg.display.update()


