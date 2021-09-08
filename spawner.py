import pygame
from hero import Hero

entities = pygame.image.load('images/entities.png')


class Spawner(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.hp = 3
        self.image = entities.subsurface((32 * 32 + (3 - self.hp) * 32, type * 32, 32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))

    def spawn(self):
        return Hero(self.type, self.rect.x + 32, self.rect.y + 32)

    def update(self):
        self.image = entities.subsurface((32 * 32 + (3 - self.hp) * 32, self.type * 32, 32, 32))
