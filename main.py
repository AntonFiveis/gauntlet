import pygame
from hero import Hero
import random

pygame.init()

heroIcon = pygame.image.load('images/gauntlet.png')
entities = pygame.image.load('images/entities.png')
backgroungs = pygame.image.load('images/backgrounds.png')

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_icon(heroIcon)

hero = Hero(2, 250, 250)

enemies = pygame.sprite.Group()
enemies.add(Hero(7, 64, 64))
enemies.add(Hero(5, 96, 64))
enemies.add(Hero(6, 64, 96))
enemies.add(Hero(4, 96, 96))

bullets = pygame.sprite.Group()

fps = 30
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

map_surface = pygame.Surface((32 * len(map[0]), 32 * len(map)))
for i in range(len(map)):
    for j in range(len(map[i])):
        map_surface.blit(backgroungs, (32 * j, 32 * i), (32, 0, 32, 32))
        if map[i][j] == 1:
            walls.append(pygame.Rect((32 * j, 32 * i, 32, 32)))

            map_surface.blit(backgroungs, (32 * j, 32 * i), (0, 32, 32, 32))


def collide(rect1, rect2):
    if rect2.colliderect(rect1):

        if 0 <= rect2.x - rect1.x + 32 < 5:
            rect1.x = rect2.x + 32
        if 0 <= rect1.x - rect2.x + 32 < 5:
            rect1.x = rect2.x - 32
        if 0 <= rect2.y - rect1.y + 32 < 5:
            rect1.y = rect2.y + 32
        if 0 <= rect1.y - rect2.y + 32 < 5:
            rect1.y = rect2.y - 32


def update():
    screen.blit(map_surface, (0, 0))
    hero.update()
    for wall in walls:
        collide(hero.rect, wall)
    for enemy in enemies:

        collide(hero.rect, enemy.rect)

        enemy.update()
        for wall in walls:
            collide(enemy.rect, wall)

        for another_enemy in enemies:
            if enemy != another_enemy:
                collide(enemy.rect, another_enemy.rect)
        collide(enemy.rect, hero.rect)

        randint = random.randint(0, 100)
        if randint > 96:
            bullet = enemy.shoot()
            if bullet:
                bullets.add(enemy.shoot())

    bullets.update()

    for bullet in bullets:
        if bullet.type > 3:
            if bullet.rect.colliderect(hero.rect):
                hero.hp -= 10
                bullet.kill()
        else:
            enemy = bullet.rect.collidedict(enemies.spritedict)
            if enemy:
                enemy[0].hp -= 10
                if enemy[0].hp <= 0:
                    enemy[0].kill()
                bullet.kill()
        if bullet.rect.collidelist(walls) != -1:
            bullet.kill()
        another_bullet = bullet.rect.collidedict(bullets.spritedict)
        if another_bullet and another_bullet[0] != bullet:
            bullet.kill()
            another_bullet[0].kill()
        if bullet.rect.x > width + 16 or bullet.rect.y > height + 16 or bullet.rect.x < -16 or bullet.rect.y < -16:
            bullet.kill()

    screen.blit(hero.image, hero.rect)
    enemies.draw(screen)
    bullets.draw(screen)

    pygame.display.update()


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
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                hero.setYChange(0)
            if event.key == pygame.K_d or event.key == pygame.K_a:
                hero.setXChange(0)
    for enemy in enemies:
        if enemy.rect.x < hero.rect.x - 16:
            enemy.setXChange(1)
        elif enemy.rect.x > hero.rect.x + 16:
            enemy.setXChange(-1)
        else:
            enemy.setXChange(0)
        if enemy.rect.y < hero.rect.y - 16:
            enemy.setYChange(1)
        elif enemy.rect.y > hero.rect.y + 16:
            enemy.setYChange(-1)
        else:
            enemy.setYChange(0)
    update()
    clock.tick(fps)
