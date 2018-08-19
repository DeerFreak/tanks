import pygame
from colors import *
import pygame

class tank(object):
    def __init__(self, start_pos, surf):
        self.surf = surf
        self.alive = True

        self.moving = False
        self.xlen = 100
        self.ylen = 60
        self.cannonlen = 70
        self.angle = 0
        self.pos = [start_pos[0], start_pos[1]]

        img = "tank_red.png"
        self.cross = pygame.image.load(img).convert_alpha()
        self.toRotate = self.cross.copy()

    def move(self):
        if self.moving == False:
            return

    def plot(self, angle):
        self.toRotate = pygame.transform.rotate(self.cross, angle)
        rect = self.toRotate.get_rect(center=(self.pos[0],self.pos[1]))
        self.surf.blit(self.toRotate,rect)


if __name__ == '__main__':
    pygame.init()
    surf = pygame.display.set_mode((1000, 1000), 0, 32)
    panzer = tank((500, 500), surf)
    a = 0
    while True:
        a += 0.1
        surf.fill((255, 255, 255))
        panzer.plot(a)
        pygame.display.update()
