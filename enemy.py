class Enemy:

    def __init__(self, type, x, y):
        if type == 'ghost':
            self.hp = 1
            self.speed = 0.5
        elif type == 'demon':
            self.hp = 2
            self.speed = 0.7
        self.x = x
        self.y = y