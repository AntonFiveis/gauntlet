import pygame

heroes = pygame.image.load('images/entities.png')


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


class Hero:
    def __init__(self, type, x, y):
        # warrior
        if type == 0:
            self.hp = 100
            self.speed = 6
        # valk
        elif type == 1:
            self.hp = 200
            self.speed = 6
        # wizard
        elif type == 2:
            self.hp = 200
            self.speed = 6
        # rogue
        elif type == 3:
            self.hp = 200
            self.speed = 6
        # ghost
        elif type == 4:
            self.hp = 200
            self.speed = 4
        # demon
        elif type == 5:
            self.hp = 200
            self.speed = 4
        # big BOOOOYYYYYYYYYY
        elif type == 6:
            self.hp = 200
            self.speed = 4
        # rogue
        elif type == 7:
            self.hp = 200
            self.speed = 4
        # rogue
        elif type == 8:
            self.hp = 200
            self.speed = 4
        self.x_change = 0
        self.y_change = 0
        self.type = type
        self.x = x
        self.y = y
        self.sprite = 0
        self.direction = 4

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
        self.x += self.x_change
        self.y += self.y_change

    def display(self, screen):
        screen.blit(heroes, (self.x, self.y), (32 * (self.sprite//10 * 8 + self.direction), self.type * 32, 32, 32))

    def shoot(self):
        print('shoot')

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
