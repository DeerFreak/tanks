WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
import pygame
import time

surf = pygame.display.set_mode((400, 400))

org_img = pygame.image.load("tank_red.png")
surf.blit(org_img, (200, 200))
angle = 0
rect = org_img.get_rect()
img = org_img

while True:
    angle += 0.05 % 360
    surf.fill((0,0,0))
    img = pygame.transform.rotate(org_img, angle)
    rect = img.get_rect()
    surf.blit(img, rect)
    pygame.display.update()