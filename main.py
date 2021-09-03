import pygame

pygame.init()
heroIcon = pygame.image.load('images/gauntlet.png')
heroes = pygame.image.load("images/entities.png")

screen = pygame.display.set_mode((800, 600))
pygame.display.set_icon(heroIcon)
x, y = 200, 200
ex, ey = 0, 0
xChange, yChange = 0, 0
screen.fill((0, 0, 0))
enemySpeed = 0.07
heroSpeed = 0.1
sprite = 0


def displayHero(heroX, heroY):
    screen.blit(heroes, (heroX, heroY), ((sprite//1000+1)*32*8, 0, 32, 32))


def displayEnemy(enemyX, enemyY):
    screen.blit(heroes, (enemyX, enemyY), (0, 0, 32, 32))


# def shoot(shootX, shoo)
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                yChange = -heroSpeed
            if event.key == pygame.K_s:
                yChange = heroSpeed
            if event.key == pygame.K_d:
                xChange = heroSpeed
            if event.key == pygame.K_a:
                xChange = -heroSpeed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                yChange = 0
            if event.key == pygame.K_d or event.key == pygame.K_a:
                xChange = 0
    if ex < x:
        ex += enemySpeed
    elif ex > x:
        ex -= enemySpeed
    if ey < y:
        ey += enemySpeed
    elif ey > y:
        ey -= enemySpeed
    sprite += 1
    if sprite > 2000:
        sprite = 0
    print(sprite)
    x += xChange
    y += yChange
    displayHero(x, y)
    displayEnemy(ex, ey)
    pygame.display.update()
