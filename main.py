import pygame
from hero import Hero
from gate import Gate
from item import Item
from spawner import Spawner
import random

pygame.init()
f = pygame.font.SysFont('arial', 30)
pygame.time.set_timer(pygame.USEREVENT, 1500)
heroIcon = pygame.image.load('images/gauntlet.png')
entities = pygame.image.load('images/entities.png')
backgroungs = pygame.image.load('images/backgrounds.png')

pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
running = True
pygame.display.set_icon(heroIcon)

hero_type = -1
keys = 0
score = 0
potions = 0
invulnerability = 0
level = 0
enemies = pygame.sprite.Group()

gates = pygame.sprite.Group()
items = pygame.sprite.Group()
spawners = pygame.sprite.Group()
bullets = pygame.sprite.Group()

fps = 60
clock = pygame.time.Clock()

while hero_type == -1 and running:

    screen.blit(f.render('Choose your hero :0-warrior,1-valk,2-wizard,3-rogue' , 1, (255, 255, 255)), (width//2-250, height//2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                hero_type = 0
            if event.key == pygame.K_1:
                hero_type = 1
            if event.key == pygame.K_2:
                hero_type = 2
            if event.key == pygame.K_3:
                hero_type = 3
    pygame.display.update()
    clock.tick(fps)
walls = []
Map = [[
    'wwwwwwwwwwwwwwwwwwww',
    'wh     k wE        wwwwwwww',
    'w        w      G       www',
    'wwwwwwlllw              www',
    'ws  B    wwwwwllllwwwwwwwww',
    'w        w                w',
    'ws       w           f    w',
    'w        w         wwwwwwww',
    'w                  ws    kw',
    'w                  w  W   w',
    'w        w  d      w      w',
    'w  p    w w               w',
    'wwwwwwwwwwwwwwwwwwwwwwwwwww'
]

    , [
        'wwwwwwwwwwwwwwwwwwww',
        'wh       wE        wwwwwwww',
        'w        w      G       www',
        'wwwwww   w              www',
        'ws  B    wwwwwllllwwwwwwwww',
        'w        w                w',
        'ws       w     p     f    w',
        'w   B    w         wwwwwwww',
        'w            B     ws    kw',
        'w    p             w  W   w',
        'w        w  d      w      w',
        'w  p    w w               w',
        'wwwwwwwwwwwwwwwwwwwwwwwwwww'
    ]

    , [
        'wwwwwwwwwwwwwwwwwwww',
        'wh       wf        wwwwwwww',
        'w        w      G       www',
        'w        w              www',
        'ws   wwwwwwwww    wwwwwwwww',
        'w    gg swww              w',
        'wwwwww   wwwp        f    w',
        'w d d     ww       wwwwwwww',
        'w     b    w       ws    kw',
        'w  d               w  W   w',
        'w        w  d   l         w',
        'w  p    w w               w',
        'w                         w',
        'wllllllwwwlllllwwwllllwwwww',
        'w       G  G  G  G        w',
        'w                         w',
        'w         G G G           w',
        'w           E             w',
        'wwwwwwwwwwwwwwwwwwwwwwwwwww'
    ]]


def findAllGates(y, x):
    s = list(Map[level][y])
    s[x] = 'o'
    Map[level][y] = "".join(s)
    if x + 1 < len(Map[level][y]) and Map[level][y][x + 1] == 'l':
        return findAllGates(y, x + 1)
    elif y + 1 < len(Map[level]) and Map[level][y + 1][x] == 'l':
        return findAllGates(y + 1, x)
    else:
        return y, x

def next_level():
    global map_surface, walls, enemies, spawners, items, gates, bullets

    walls = []
    gates = pygame.sprite.Group()
    items = pygame.sprite.Group()
    spawners = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    map_surface = draw_map()
def draw_map():
    global hero
    map_surface = pygame.Surface((32 * max(map(lambda row: len(row), Map[level])), 32 * len(Map[level])))
    for i in range(len(Map[level])):
        for j in range(len(Map[level][i])):
            map_surface.blit(backgroungs, (32 * j, 32 * i), (32, 0, 32, 32))
            if Map[level][i][j] == 'w':
                walls.append(pygame.Rect((32 * j, 32 * i, 32, 32)))

                map_surface.blit(backgroungs, (32 * j, 32 * i), (0, 32, 32, 32))
            elif Map[level][i][j] == 'l':
                y_end, x_end = findAllGates(i, j)
                gates.add(Gate(j, i, x_end, y_end))
            elif Map[level][i][j] == 'k':
                items.add(Item(j * 32, i * 32, 5))
            elif Map[level][i][j] == 'f':
                items.add(Item(j * 32, i * 32, random.randint(0, 4)))
            elif Map[level][i][j] == 'p':
                items.add(Item(j * 32, i * 32, 6))
            elif Map[level][i][j] == 'E':
                items.add(Item(j * 32, i * 32, 12))
            elif Map[level][i][j] == 's':
                items.add(Item(j * 32, i * 32, random.randint(7, 9)))
            elif Map[level][i][j] == 'h':
                hero = Hero(hero_type, 32 * j, 32 * i)
            elif Map[level][i][j] == 'g':
                enemies.add(Hero(4, 32 * j, 32 * i))
            elif Map[level][i][j] == 'd':
                enemies.add(Hero(5, 32 * j, 32 * i))
            elif Map[level][i][j] == 'b':
                enemies.add(Hero(6, 32 * j, 32 * i))
            elif Map[level][i][j] == 'e':
                enemies.add(Hero(7, 32 * j, 32 * i))
            elif Map[level][i][j] == 'r':
                enemies.add(Hero(8, 32 * j, 32 * i))
            elif Map[level][i][j] == 'G':
                spawners.add(Spawner(4, 32 * j, 32 * i))
            elif Map[level][i][j] == 'D':
                spawners.add(Spawner(5, 32 * j, 32 * i))
            elif Map[level][i][j] == 'B':
                spawners.add(Spawner(6, 32 * j, 32 * i))
            elif Map[level][i][j] == 'W':
                spawners.add(Spawner(7, 32 * j, 32 * i))
    return map_surface


def collide(rect1, rect2):
    if rect2.colliderect(rect1):

        if 0 <= rect2.x - rect1.x + 32 <hero_type+4:
            rect1.x = rect2.x + 32
        elif 0 <= rect1.x - rect2.x + 32 < hero_type+4:
            rect1.x = rect2.x - 32
        if 0 <= rect2.y - rect1.y + 32 < hero_type+4:
            rect1.y = rect2.y + 32
        elif 0 <= rect1.y - rect2.y + 32 < hero_type+4:
            rect1.y = rect2.y - 32


def update():
    global keys, potions, score, running, invulnerability, level
    screen.blit(map_surface, (0, 0))
    hero.update()
    for wall in walls:
        collide(hero.rect, wall)
    for gate in gates:

        if keys == 0:
            collide(hero.rect, gate.rect)
        else:
            if gate.rect.colliderect(hero.rect):
                keys -= 1
                gate.kill()
    for spawner in spawners:
        collide(hero.rect, spawner.rect)

    for enemy in enemies:

        collide(hero.rect, enemy.rect)

        enemy.update()
        for wall in walls:
            collide(enemy.rect, wall)
        for gate in gates:
            collide(enemy.rect, gate.rect)
        for spawner in spawners:
            collide(enemy.rect, spawner.rect)
        for another_enemy in enemies:
            if enemy != another_enemy:
                collide(enemy.rect, another_enemy.rect)
        if enemy.rect.colliderect(hero.rect):
            if invulnerability == 0:
                hero.hp -= 10
                invulnerability = 120
        collide(enemy.rect, hero.rect)

        randint = random.randint(0, 100)
        if randint > 96:
            bullet = enemy.shoot()
            if bullet:
                bullets.add(enemy.shoot())

    for item in items:
        if item.rect.colliderect(hero.rect):
            if item.type < 5:
                hero.hp += 50
            elif item.type == 5:
                keys = keys + 1
            elif item.type == 6:
                potions = potions + 1
            elif item.type < 10:
                score = score + 100
            elif item.type == 12:
                level += 1

                if level > 2:
                    running = False
                else:
                    next_level()
            item.kill()

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

            spawner = bullet.rect.collidedict(spawners.spritedict)
            if spawner:
                spawner[0].hp -= 1
                if spawner[0].hp <= 0:
                    spawner[0].kill()
                bullet.kill()
        if bullet.rect.collidelist(walls) != -1:
            bullet.kill()
        if bullet.rect.collidedict(gates.spritedict):
            bullet.kill()
        another_bullet = bullet.rect.collidedict(bullets.spritedict)
        if another_bullet and another_bullet[0] != bullet:
            bullet.kill()
            another_bullet[0].kill()
        if bullet.rect.x > width + 16 or bullet.rect.y > height + 16 or bullet.rect.x < -16 or bullet.rect.y < -16:
            bullet.kill()

    items.draw(screen)
    screen.blit(hero.image, hero.rect)
    spawners.update()
    spawners.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)
    gates.draw(screen)

    screen.blit(f.render('Score:' + str(score), 1, (255, 255, 255)), (16, 16))
    screen.blit(f.render('Potions:' + str(potions), 1, (255, 255, 255)), (16, 48))
    screen.blit(f.render('HP:' + str(hero.hp), 1, (255, 255, 255)), (16, 80))
    screen.blit(f.render('Keys:' + str(keys), 1, (255, 255, 255)), (16, 112))

    if invulnerability > 0:
        invulnerability -= 1


map_surface = draw_map()
while running:
    screen.fill((0, 0, 0))
    if hero.hp>0:
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
                if event.key == pygame.K_f:
                    if potions > 0:
                        potions -= 1
                        x, y = pygame.mouse.get_pos()
                        explosion = pygame.Rect((x - 80, y - 80, 160, 160))
                        for enemy in enemies:
                            if explosion.colliderect(enemy.rect):
                                enemy.kill()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    hero.setYChange(0)
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    hero.setXChange(0)
            elif event.type == pygame.USEREVENT:
                for spawner in spawners:
                    enemies.add(spawner.spawn())
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
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(f.render('Score:'+str(score), 1, (255,255,255)), (160,160))
    clock.tick(fps)
    pygame.display.update()
