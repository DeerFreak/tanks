import pygame
import sys
import time as t
from colors import *
from pygame.locals import *
import numpy as np
from stats import bullets, resolution
from tank_class import Tank


class App(object):
    def __init__(self, surf, FPS):
        self.surf = surf
        self.all_sprites = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        tank_stats = {"red": (resolution[0] / 4, resolution[1] / 4),
                      "blue": (3 * resolution[0] / 4, 3 * resolution[1] / 4)}
        self.tank1 = Tank(tank_stats["red"], self.surf, "red")
        self.tank2 = Tank(tank_stats["blue"], self.surf, "blue")
        self.tank2_group = pygame.sprite.Group()
        self.tank2_group.add(self.tank2)
        self.all_sprites.add(self.tank1)
        self.all_sprites.add(self.tank2)
        self.tanks.add(self.tank1)
        self.tanks.add(self.tank2)

        self.running = True
        self.delta_frame = 1 / FPS
        self.event_dict = {"w": False, "a": False, "s": False, "d": False, " ": False,
                           "đ": False, "ē": False, "Ē": False, "Ĕ": False, "p": False,
                           "c": False, "o": False}
        self.event_keys = {"c": self.tank1.next_weapon,
                           "o": self.tank2.next_weapon,
                           "č": pygame.quit}  # Quit on "-" num block
        self.last_fire = [0, 0]
        self.last_reload = [0, 0]

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
                self.check_bullet_hit()
                self.plot()
                if self.tank1.health <= 0 or self.tank2.health <= 0:
                    self.running = False

    def events(self):
        # Panzer1: WASD und Space
        # Panzer2: Pfeiltasten und P
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
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
        collision = pygame.sprite.spritecollide(self.tank1, self.tank2_group, False,
                                                pygame.sprite.collide_rect_ratio(0.9))
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
        hits1 = pygame.sprite.spritecollide(self.tank1, self.bullets, False)
        hits2 = pygame.sprite.spritecollide(self.tank2, self.bullets, False)
        for _ in hits1:
            self.tank1.health -= 20
        for _ in hits2:
            self.tank2.health -= 20

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
                bullet = self.tank1.fire()
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
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
                bullet = self.tank2.fire()
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
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


