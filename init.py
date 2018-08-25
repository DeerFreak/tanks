import pygame
from colors import *
from tank_class import *
from stats import *
import time


def initialize_game():
    pg.init()
    if FULLSCREEN:
        surf = pygame.display.set_mode((RESOLUTION[0], RESOLUTION[1]), pygame.FULLSCREEN)
    else:
        surf = pygame.display.set_mode((RESOLUTION[0], RESOLUTION[1]))
    pygame.display.set_caption(NAME)
    game_icon = pygame.image.load('icon.png')
    pygame.display.set_icon(game_icon)
    
    surf.fill(WHITE)
    pygame.display.update()

    return surf

