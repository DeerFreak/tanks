import pygame
from colors import *

class tank(object):
    def __init__(self, start_pos, surf, color):
        self.surf = surf
        self.alive = True

        self.moving = False
        self.xlen = 100
        self.ylen = 60
        self.cannonlen = 70
        self.angle = 0
        self.pos = [start_pos[0], start_pos[1]]
        
        if color == "red":
            img = "tank_red.png"
        else:
            img = "tank_blue.png"
        self.cross = pygame.image.load(img).convert_alpha()
        self.toRotate = self.cross.copy()

    def move(self):
        if self.moving == False:
            return

    def plot(self, angle):
        self.toRotate = pygame.transform.rotate(self.cross, angle)
        rect = self.toRotate.get_rect(center=(self.pos[0],self.pos[1]))
        self.surf.blit(self.toRotate,rect)


