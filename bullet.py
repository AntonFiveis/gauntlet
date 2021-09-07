import pygame

bullets = pygame.image.load('images/entities.png')


class Bullet(pygame.sprite.Sprite):
    speed = 15

    def __init__(self, x, y, type, direction):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.direction = direction
        self.x_change = 0
        self.y_change = 0
        if direction != 4 and direction != 0:
            self.x_change = self.speed * (4 - direction) / abs(4 - direction)
        if 2 < direction < 6:
            self.y_change = self.speed
        elif direction < 2 or direction == 7:
            self.y_change = -self.speed
        self.image = bullets.subsurface((32 * (3 * 8 + self.direction), self.type * 32, 32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        # if self.x > 800:
        #     self.x = 0
        # if self.y > 600:
        #     self.y = 0
        # if self.x < 0:
        #     self.x = 800
        # if self.y < 0:
        #     self.y = 600

