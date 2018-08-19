import pygame
from pygame.locals import *
import sys

img = "tank_red.png"

pygame.init()

screen = pygame.display.set_mode((320,240), 0, 32)
pygame.display.set_caption("transform.rotate - Test")

cross = pygame.image.load(img).convert_alpha()
toRotate = pygame.Surface((128,128))
toRotate = cross.copy()
angle = 0

while True:
    angle += 0.01
    toRotate = pygame.transform.rotate(cross, angle)

    rect = toRotate.get_rect(center=(100,100))
    screen.fill((0,0,255))
    screen.blit(toRotate,rect)
    pygame.display.update()