import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos0, angle0, surf):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos0[:]
        self.angle = angle0
        self.image = pygame.image.load("wall.png")
        self.rect = self.image.get_rect()
        self.surf = surf
        self.mask = pygame.mask.from_surface(self.image)

    def plot(self):
        self.surf.blit(self.image, self.mask)
