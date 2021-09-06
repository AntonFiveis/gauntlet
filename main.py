import pygame
from hero import Hero

fps = 60
pygame.init()
heroIcon = pygame.image.load('images/gauntlet.png')
heroes = pygame.image.load("images/entities.png")

screen = pygame.display.set_mode((800, 600))
pygame.display.set_icon(heroIcon)
x, y = 200, 200
ex, ey = 0, 0
xChange, yChange = 0, 0
screen.fill((0, 0, 0))

hero = Hero(3, 250, 250)
enemy = Hero(7, 0, 0)

def update():
    hero.update()
    hero.display(screen)
    enemy.update()
    enemy.display(screen)

# def shoot(shootX, shoo)
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                hero.setYChange(-1)
            if event.key == pygame.K_s:
                hero.setYChange(1)
            if event.key == pygame.K_d:
                hero.setXChange(1)
            if event.key == pygame.K_a:
                hero.setXChange(-1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                hero.setYChange(0)
            if event.key == pygame.K_d or event.key == pygame.K_a:
                hero.setXChange(0)
    if enemy.x < hero.x+8:
        enemy.setXChange(1)
    elif enemy.x > hero.x-8:
        enemy.setXChange(-1)
    else:
        enemy.setXChange(0)
    if enemy.y < hero.y-8:
        enemy.setYChange(1)
    elif enemy.y > hero.y+8:
        enemy.setYChange(-1)
    else:
        enemy.setYChange(0)
    enemy.update()
    enemy.display(screen)
    hero.update()
    hero.display(screen)
    pygame.display.update()
    pygame.time.delay(1000 // fps)
