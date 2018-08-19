import pygame
from colors import *
import tank_class

def initialize_game(resolution):
    surf = pygame.display.set_mode((resolution[0], resolution[1]), pygame.FULLSCREEN)
    pygame.display.fill(WHITE)
    pygame.display.update()
    tanks = []
    for i in [(200, 500), (800, 600)]:
        tanks.append(tank(i, surf))
    return (surf, tanks)



