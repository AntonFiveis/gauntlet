import pygame
from bullet import Bullet

entities = pygame.image.load('images/entities.png')


def calculate_direction(x_change, y_change):
    if x_change > 0:
        if y_change < 0:
            return 1
        elif y_change == 0:
            return 2
        else:
            return 3
    elif x_change == 0:
        if y_change < 0:
            return 0
        elif y_change > 0:
            return 4
    else:
        if y_change < 0:
            return 7
        elif y_change == 0:
            return 6
        else:
            return 5


class Hero(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        pygame.sprite.Sprite.__init__(self)
        # warrior
        if type == 0:
            self.hp = 300
            self.speed = 2
        # valk
        elif type == 1:
            self.hp = 250
            self.speed = 3
        # wizard
        elif type == 2:
            self.hp = 200
            self.speed = 4
        # rogue
        elif type == 3:
            self.hp = 100
            self.speed = 5
        # ghost
        elif type == 4:
            self.hp = 10
            self.speed = 1
        # demon
        elif type == 5:
            self.hp = 20
            self.speed = 1
        # big BOOOOYYYYYYYYYY
        elif type == 6:
            self.hp = 30
            self.speed = 2
        # wizard enemy
        elif type == 7:
            self.hp = 30
            self.speed = 2
        # rogue
        elif type == 8:
            self.hp = 30
            self.speed = 2
        self.x_change = 0
        self.y_change = 0
        self.type = type
        self.sprite = 0
        self.direction = 4
        self.image = entities.subsurface((
            32 * (self.sprite // 10 * 8 + self.direction), self.type * 32, 32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))

    def changeSprite(self):
        if self.x_change != 0 or self.y_change != 0:
            direction = calculate_direction(self.x_change, self.y_change)
            if self.direction == direction:
                self.sprite += 1
                if self.sprite > 29:
                    self.sprite = 10
            else:
                self.sprite = 10
                self.direction = direction
        else:
            self.sprite = 0
        self.image = entities.subsurface((
            32 * (self.sprite // 10 * 8 + self.direction), self.type * 32, 32, 32))

    def update(self):
        self.changeSprite()
        if self.x_change == 0 and self.y_change == 0:
            return
        if self.direction != 4 and self.direction != 0:
            self.x_change = self.speed * (4 - self.direction) / abs(4 - self.direction)
        if 2 < self.direction < 6:
            self.y_change = self.speed
        elif self.direction < 2 or self.direction == 7:
            self.y_change = -self.speed
        self.rect.x += self.x_change
        self.rect.y += self.y_change

    def shoot(self):
        if self.type < 4 or self.type == 5 or self.type == 7:
            return Bullet(self.rect.x, self.rect.y, self.type, self.direction)

    def setXChange(self, x_change):
        if x_change == 0:
            self.x_change = 0
            return
        self.x_change = x_change / abs(x_change) * self.speed

    def setYChange(self, y_change):
        if y_change == 0:
            self.y_change = 0
            return
        self.y_change = y_change / abs(y_change) * self.speed
