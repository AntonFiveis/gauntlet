import pygame

entities = pygame.image.load('images/entities.png')


class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y, x_end, y_end):
        pygame.sprite.Sprite.__init__(self)
        if x_end - x > y_end - y:
            self.image = pygame.Surface(((x_end+1 - x)*32, 32), pygame.SRCALPHA, 32)
            for i in range(x_end - x+1):
                self.image.blit(entities, (i * 32, 0), (10 * 32, 9 * 32, 32, 32))
        else:
            self.image = pygame.Surface((32, (y_end+1 - y)*32), pygame.SRCALPHA, 32)
            for i in range(y_end - y+1):
                self.image.blit(entities, (0, i * 32), (11 * 32, 9 * 32, 32, 32))
        self.rect = self.image.get_rect(topleft=(x*32, y*32))
