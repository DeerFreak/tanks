import pygame as pg
import sys
import time as t
from colors import *
from pygame.locals import *
import numpy as np
from stats import bullets


class App(object):
    def __init__(self, game, FPS):
        self.surf = game[0]
        self.tank1 = game[1][0]
        self.tank2 = game[1][1]
        self.bullets = []
        self.running = True
        self.delta_frame = 1 / FPS
        self.event_dict = {"w": False, "a": False, "s": False, "d": False, " ": False,
                           "đ": False, "ē": False, "Ē": False, "Ĕ": False, "p": False,
                           "c": False, "o": False}
        self.event_keys = {"c": self.tank1.next_weapon,
                           "o": self.tank2.next_weapon,
                           "č": pg.quit}  # Quit on "-" num block
        self.last_fire = None
        self.last_reload = None
        self.init_game_stats()

    def init_game_stats(self):
        (self.last_fire, self.last_reload) = ([0, ] * 2,) * 2

    def start(self):
        time = t.time()
        while self.running:
            if (t.time() - time) >= self.delta_frame:
                time = t.time()
                self.events() 
                self.tank_key_assignment() 
                self.tank_move()
                self.bullet_move()
                self.check_tank_collision()
                self.plot()

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

    def check_tank_collision(self): # tank collision
        dist = np.linalg.norm(np.asarray(self.tank1.pos)-np.asarray(self.tank2.pos)) # dist tank centers
        dist_min = np.linalg.norm(np.asarray([87,54])) # radius of wides possible circle around tank
        if dist < 0.8*dist_min: # 0.8 is factor to prevent unrealistic distance of collision
            if self.event_dict["w"]:
                self.tank1.moving = -1
            elif self.event_dict["s"]:
                self.tank1.moving = 1
            if self.event_dict["đ"]:
                self.tank2.moving = -1
            elif self.event_dict["Ē"]:
                self.tank2.moving = 1
            self.tank1.move()
            self.tank2.move()

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
            temp = bullets[self.tank1.loaded_weapons[self.tank1.current_weapon]]["reload_time"]
            if (t.time() - self.last_fire[0]) >= temp:
                self.bullets.append(self.tank1.fire())
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
            temp = bullets[self.tank2.loaded_weapons[self.tank2.current_weapon]]["reload_time"]
            if (t.time() - self.last_fire[1]) >= temp:
                self.bullets.append(self.tank2.fire())
                self.last_fire[1] = t.time()

    def tank_move(self):
        self.tank1.move()
        self.tank2.move()
    
    def bullet_move(self):
        for bullet in self.bullets:
            bullet.move()

    def plot(self):
        self.surf.fill(WHITE)
        self.tank1.plot()
        self.tank2.plot()
        for bullet in self.bullets:
            bullet.plot()

        pg.display.update()


