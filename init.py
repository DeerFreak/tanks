import pygame
from colors import *
from tank_class import *
from stats import resolution
import time

def initialize_game(resolution, fullscreen):
    if fullscreen:
        surf    = pygame.display.set_mode((resolution[0], resolution[1]), pygame.FULLSCREEN)
    else:
        surf    = pygame.display.set_mode((resolution[0], resolution[1]))
    pygame.display.set_caption('Tank Game')
    game_icon   = pygame.image.load('icon.png')
    pygame.display.set_icon(game_icon)
    
    surf.fill(WHITE)
    pygame.display.update()
    
    tanks       = []
    stats       = {"red":(resolution[0] / 4, resolution[1] / 4), "blue": (3 * resolution[0] / 4, 3 * resolution[1] / 4)}
    
    for i in stats.keys():
        tanks.append(Tank(stats[i], surf, i))
   
    return (surf, tanks)

