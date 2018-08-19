import pygame
import math as m
from colors import *

class tank(object):
    def __init__(self, start_pos, surf, color):
        self.surf = surf
        self.alive = True

        self.speed = 5
        self.moving = 0
        self.gear = {0:0, 1:self.speed, -1:-self.speed}
        self.angle = 0
        self.pos = [start_pos[0], start_pos[1]]
        
        if color == "red":
            img = "tank_red.png"
        else:
            img = "tank_blue.png"
        #self.cross = pygame.image.load(img).convert_alpha()
        #self.toRotate = self.cross.copy()

    def move(self):
        self.pos[0] += int(m.cos(self.angle) * self.gear[self.moving])
        self.pos[1] += int(m.sin(self.angle) * self.gear[self.moving])
        

    def plot(self):
        self.toRotate = pygame.transform.rotate(self.cross, self.angle)
        rect = self.toRotate.get_rect(center=(self.pos[0],self.pos[1]))
        self.surf.blit(self.toRotate,rect)


tank = tank((100, 100), 3, "red")
tank.moving = 1
tank.angle = m.pi / 4
for i in range(10):
    tank.move()
    print(tank.pos)