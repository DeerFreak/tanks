import pygame
import sys
import time
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


