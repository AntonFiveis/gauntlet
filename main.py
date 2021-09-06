import pygame
from hero import Hero
import random

fps = 60
pygame.init()
heroIcon = pygame.image.load('images/gauntlet.png')
entities = pygame.image.load('images/entities.png')
backgroungs = pygame.image.load('images/backgrounds.png')
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_icon(heroIcon)
hero = Hero(3, 250, 250)
enemies = [Hero(7, 0, 0), Hero(6, 600, 0), Hero(5, 0, 500), Hero(4, 600, 500)]
bullets = []
# enemies = []
delay = 30
clock = pygame.time.Clock()
map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

def update():
    for i in range(len(map)):
        for j in range(len(map[i])):
            screen.blit(backgroungs,(32*j, 32*i), (32,0,32,32))
            if map[i][j]!=0:
                if i==0 or i==len(map)-1:
                    screen.blit(entities, (32*j, 32*i), (10*32,9*32,32,32 ))
                else:
                    screen.blit(entities, (32*j, 32*i), (11*32,9*32,32,32 ))

    hero.update()
    hero.display(screen)
    for enemy in enemies:
        randint = random.randint(0, 100)
        if randint > 98:
            bullet = enemy.shoot()
            if bullet:
                bullets.append(enemy.shoot())
        enemy.update()
        enemy.display(screen)
    for bullet in bullets:
        bullet.update()
        bullet.display(screen)
        if bullet.x > width+16 or bullet.y > height+16 or bullet.x < -16 or bullet.y < -16:
            bullets.remove(bullet)
    pygame.display.update()


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
            if event.key == pygame.K_SPACE:
                bullets.append(hero.shoot())
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                hero.setYChange(0)
            if event.key == pygame.K_d or event.key == pygame.K_a:
                hero.setXChange(0)
    for enemy in enemies:
        if enemy.x < hero.x + 8:
            enemy.setXChange(1)
        elif enemy.x > hero.x - 8:
            enemy.setXChange(-1)
        else:
            enemy.setXChange(0)
        if enemy.y < hero.y - 8:
            enemy.setYChange(1)
        elif enemy.y > hero.y + 8:
            enemy.setYChange(-1)
        else:
            enemy.setYChange(0)
    update()
    clock.tick(fps)
