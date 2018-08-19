import pygame
from colors import *
from tank_class import *

import time

def initialize_game(resolution):
    surf = pygame.display.set_mode((resolution[0], resolution[1]))
    surf.fill(WHITE)
    pygame.display.update()
    tanks = []
    stats = {"red":(200, 500), "blue": (800, 600)}
    for i in stats.keys():
        tanks.append(Tank(stats[i], surf, i))
    return (surf, tanks)

