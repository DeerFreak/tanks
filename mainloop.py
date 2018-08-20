import pygame
import sys
import time as t
from colors import *
from pygame.locals import *
import numpy as np
from stats import bullets

class App(object):
    def __init__(self, game, FPS):
        self.surf       = game[0]
        self.tank1      = game[1][0]
        self.tank2      = game[1][1]
        self.bullets    = []
        self.running    = True
        self.delta_frame       = 1 / FPS
        self.event_dict = { "W": False, "A": False, "S": False, "D": False, "Space": False,
                            "PO": False, "PL": False, "PU": False, "PR": False, "P": False}
        self.init_game_stats()

    def init_game_stats(self):
        self.last_fire = [0,] * 2

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
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.event_dict["PO"] = True
                if event.key == K_DOWN:
                    self.event_dict["PU"] = True
                if event.key == K_LEFT:
                    self.event_dict["PL"] = True
                if event.key == K_RIGHT:
                    self.event_dict["PR"] = True
                if event.key == K_w:
                    self.event_dict["W"] = True
                if event.key == K_a:
                    self.event_dict["A"] = True
                if event.key == K_s:
                    self.event_dict["S"] = True
                if event.key == K_d:
                    self.event_dict["D"] = True
                if event.key == K_SPACE:
                    self.event_dict["Space"] = True
                if event.key == K_p:
                    self.event_dict["P"] = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == KEYUP:
                if event.key == K_UP:
                    self.event_dict["PO"] = False
                if event.key == K_DOWN:
                    self.event_dict["PU"] = False
                if event.key == K_LEFT:
                    self.event_dict["PL"] = False
                if event.key == K_RIGHT:
                    self.event_dict["PR"] = False
                if event.key == K_w:
                    self.event_dict["W"] = False
                if event.key == K_a:
                    self.event_dict["A"] = False
                if event.key == K_s:
                    self.event_dict["S"] = False
                if event.key == K_d:
                    self.event_dict["D"] = False
                if event.key == K_SPACE:
                    self.event_dict["Space"] = False
                if event.key == K_p:
                    self.event_dict["P"] = False


    def check_tank_collision(self): # tank collision
        dist = np.linalg.norm(np.asarray(self.tank1.pos)-np.asarray(self.tank2.pos)) # dist tank centers
        dist_min = np.linalg.norm(np.asarray([87,54])) # radius of wides possible circle around tank
        if dist < 0.8*dist_min: # 0.8 is factor to prevent unrealistic distance of collision
            if self.event_dict["W"] == True:
                self.tank1.moving = -1
            elif self.event_dict["S"] == True:
                self.tank1.moving = 1
            if self.event_dict["PO"] == True:
                self.tank2.moving = -1
            elif self.event_dict["PU"] == True:
                self.tank2.moving = 1
            self.tank1.move()
            self.tank2.move()

    def tank_key_assignment(self):
        self.tank1_key_assignment()
        self.tank2_key_assignment()

    def tank1_key_assignment(self):
        if self.event_dict["W"] == True:
            self.tank1.moving = 1
        elif self.event_dict["S"] == True:
            self.tank1.moving = -1
        elif self.event_dict["W"] == False and self.event_dict["S"] == False:
            self.tank1.moving = 0
        if self.event_dict["A"] == True:
            self.tank1.calc_angle(-1)
        if self.event_dict["D"] == True:
            self.tank1.calc_angle(+1)
        if self.event_dict["Space"] == True:
            if (t.time() - self.last_fire[0]) >= bullets["normal"]["reload_time"]:
                self.bullets.append(self.tank1.fire())
                self.last_fire[0] = t.time()

    def tank2_key_assignment(self):
        if self.event_dict["PO"] == True:
            self.tank2.moving = 1
        elif self.event_dict["PU"] == True:
            self.tank2.moving = -1
        elif self.event_dict["PO"] == False and self.event_dict["PU"] == False:
            self.tank2.moving = 0
        if self.event_dict["PL"] == True:
            self.tank2.calc_angle(-1)
        if self.event_dict["PR"] == True:
            self.tank2.calc_angle(+1)
        if self.event_dict["P"] == True:
            if (t.time() - self.last_fire[1]) >= bullets["normal"]["reload_time"]:
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

        pygame.display.update()


