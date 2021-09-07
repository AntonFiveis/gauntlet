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
enemies = pygame.sprite.Group()
enemies.add(Hero(7, 50, 0))
enemies.add(Hero(5, 0, 50))
enemies.add(Hero(6, 0, 80))
enemies.add(Hero(4, 90, 0))
bullets = pygame.sprite.Group()
delay = 30
clock = pygame.time.Clock()
walls = []
map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

map_surface = pygame.Surface((32*len(map[0]), 32*len(map)))
for i in range(len(map)):
    for j in range(len(map[i])):
        map_surface.blit(backgroungs, (32 * j, 32 * i), (32, 0, 32, 32))
        if map[i][j] != 0:
            walls.append(pygame.Rect((32 * j, 32 * i,32,32)))
            if i == 0 or i == len(map) - 1:
                map_surface.blit(entities, (32 * j, 32 * i), (10 * 32, 9 * 32, 32, 32))
            elif j == 0 or j == len(map[i]):
                map_surface.blit(entities, (32 * j, 32 * i), (11 * 32, 9 * 32, 32, 32))
            else:
                map_surface.blit(entities, (32 * j, 32 * i), (11 * 32, 9 * 32, 32, 32))
                map_surface.blit(entities, (32 * j, 32 * i), (10 * 32, 9 * 32, 32, 32))



def update():
    screen.blit(map_surface,(0,0))
    hero.update()
    screen.blit(hero.image, hero.rect)
    for enemy in enemies:
        randint = random.randint(0, 100)
        if randint > 98:
            bullet = enemy.shoot()
            if bullet:
                bullets.add(enemy.shoot())
    enemies.update()
    enemies.draw(screen)
    bullets.update()
    for bullet in bullets:
        if bullet.rect.x > width + 16 or bullet.rect.y > height + 16 or bullet.rect.x < -16 or bullet.rect.y < -16:
            bullet.kill()
    bullets.draw(screen)
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
                bullets.add(hero.shoot())
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                hero.setYChange(0)
            if event.key == pygame.K_d or event.key == pygame.K_a:
                hero.setXChange(0)
    for enemy in enemies:
        if enemy.rect.x < hero.rect.x + 8:
            enemy.setXChange(1)
        elif enemy.rect.x > hero.rect.x - 8:
            enemy.setXChange(-1)
        else:
            enemy.setXChange(0)
        if enemy.rect.y < hero.rect.y - 8:
            enemy.setYChange(1)
        elif enemy.rect.y > hero.rect.y + 8:
            enemy.setYChange(-1)
        else:
            enemy.setYChange(0)
    update()
    clock.tick(fps)
