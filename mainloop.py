import pygame
import sys
import time
from colors import *
from pygame.locals import *


def mainloop(game):
    surf = game[0]
    tank1 = game[1][0]
    tank2 = game[1][1]
    Running = True
    event_dict = {"W": False, "A": False, "S": False, "D": False, "Space": False,
                  "PO": False, "PL": False, "PU": False, "PR": False, "P": False}
    while Running:
        event_dict = events(event_dict)

        if event_dict["W"] == True:
            tank1.moving = 1
        elif event_dict["S"] == True:
            tank1.moving = -1
        elif event_dict["W"] == False and event_dict["S"] == False:
            tank1.moving = 0
        if event_dict["A"] == True:
            tank1.angle -= tank1.turn_speed
        if event_dict["D"] == True:
            tank1.angle += tank1.turn_speed

        if event_dict["PO"] == True:
            tank2.moving = 1
        elif event_dict["PU"] == True:
            tank2.moving = -1
        elif event_dict["PO"] == False and event_dict["PU"] == False:
            tank2.moving = 0
        if event_dict["PL"] == True:
            tank2.angle -= tank2.turn_speed
        if event_dict["PR"] == True:
            tank2.angle += tank2.turn_speed

        tank1.move()
        tank2.move()
        surf.fill(WHITE)
        tank1.plot()
        tank2.plot()
        pygame.display.update()


def events(event_dict):
    # Panzer1: WASD und Space
    # Panzer2: Pfeiltasten und P
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                event_dict["PO"] = True
            if event.key == K_DOWN:
                event_dict["PU"] = True
            if event.key == K_LEFT:
                event_dict["PL"] = True
            if event.key == K_RIGHT:
                event_dict["PR"] = True
            if event.key == K_w:
                event_dict["W"] = True
            if event.key == K_a:
                event_dict["A"] = True
            if event.key == K_s:
                event_dict["S"] = True
            if event.key == K_d:
                event_dict["D"] = True
            if event.key == K_SPACE:
                event_dict["Space"] = True
            if event.key == K_p:
                event_dict["P"] = True
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()


        if event.type == KEYUP:
            if event.key == K_UP:
                event_dict["PO"] = False
            if event.key == K_DOWN:
                event_dict["PU"] = False
            if event.key == K_LEFT:
                event_dict["PL"] = False
            if event.key == K_RIGHT:
                event_dict["PR"] = False
            if event.key == K_w:
                event_dict["W"] = False
            if event.key == K_a:
                event_dict["A"] = False
            if event.key == K_s:
                event_dict["S"] = False
            if event.key == K_d:
                event_dict["D"] = False
            if event.key == K_SPACE:
                event_dict["Space"] = False
            if event.key == K_p:
                event_dict["P"] = False

    return event_dict

if __name__ == "__main__":
    while True:
        pygame.display.set_mode((200,200))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_w:
                    print("w")
            if event.type == KEYUP:
                if event.key == K_w:
                    print("!w")


