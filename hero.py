import pygame

heroes = pygame.image.load('images/entities.png')


class Hero:
    def __init__(self, type, x, y):
        # warrior
        if type == 0:
            self.hp = 100
            self.speed = 1.2
        # valk
        elif type == 1:
            self.hp = 200
            self.speed = 1.2
        # wizard
        elif type == 2:
            self.hp = 200
            self.speed = 1.2
        # rogue
        elif type == 3:
            self.hp = 200
            self.speed = 1.2
        # ghost
        elif type == 4:
            self.hp = 200
            self.speed = 1.2
        # demon
        elif type == 5:
            self.hp = 200
            self.speed = 1.2
        # big BOOOOYYYYYYYYYY
        elif type == 6:
            self.hp = 200
            self.speed = 1.2
        # rogue
        elif type == 7:
            self.hp = 200
            self.speed = 1.2
        # rogue
        elif type == 8:
            self.hp = 200
            self.speed = 1.2

        self.type = type
        self.x = x
        self.y = y
        self.sprite = 0
        self.direction = 4

    def changeSprite(self, direction, move):
        if move:
            if self.direction == direction:
                self.sprite += 1
                if self.sprite > 2:
                    self.sprite = 1
            else:
                self.sprite = 1
                self.direction = direction
        else:
            self.sprite = 0
            self.direction = direction

    def display(self, screen):
        screen.blit(heroes, (self.x, self.y), (32 * (self.sprite * 8 + self.direction), self.type * 32, 32, 32))
    def shoot(self):
        print('shoot')