import pygame

entities = pygame.image.load('images/entities.png')


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = entities.subsurface((type*32, 9*32, 32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
