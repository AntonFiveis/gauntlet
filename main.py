import math
import random
import time
import csv
import pygame
import copy
from gate import Gate
from hero import Hero
from item import Item
from spawner import Spawner
from node import Node

pygame.init()
f = pygame.font.SysFont('arial', 30)
pygame.time.set_timer(pygame.USEREVENT, 1500)
heroIcon = pygame.image.load('images/gauntlet.png')
entities = pygame.image.load('images/entities.png')
backgroungs = pygame.image.load('images/backgrounds.png')

# pygame.mixer.music.load("background.wav")
# pygame.mixer.music.play(-1)

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
running = True
pygame.display.set_icon(heroIcon)

best_time = [10 ** 8, 10 ** 8, 10 ** 8]

count = 0
hero_type = 0
finding_type = 2
keys = 0
score = 0
potions = 0
invulnerability = 0
level = 0
parents = []
max_dist = 0
exit_coords = (0, 0)
turns = 3
minimax_moves = []
nearest_enemy = None
enemy_count = 0
enemy_intel = random.randint(0,10)%2==0
random_moves = {}

enemies = pygame.sprite.Group()

gates = pygame.sprite.Group()
items = pygame.sprite.Group()
spawners = pygame.sprite.Group()
bullets = pygame.sprite.Group()

fps = 60
clock = pygame.time.Clock()

while enemy_count == 0 and running:

    screen.blit(f.render('Input enemy count', 1, (255, 255, 255)),
                (width // 2 - 250, height // 2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                enemy_count = 1
            if event.key == pygame.K_2:
                enemy_count = 2
            if event.key == pygame.K_3:
                enemy_count = 3
            if event.key == pygame.K_4:
                enemy_count = 4
            if event.key == pygame.K_5:
                enemy_count = 5
            if event.key == pygame.K_6:
                enemy_count = 6
            if event.key == pygame.K_7:
                enemy_count = 7
            if event.key == pygame.K_8:
                enemy_count = 8
            if event.key == pygame.K_9:
                enemy_count = 9

    pygame.display.update()
    clock.tick(fps)

walls = []
Map = [
    ['wwwwwwwwwwwwwwwwwwww',
     'wh       wE        wwwwwwww',
     'w        w              www',
     'www      w              www',
     'ws       ww           wwwww',
     'w                         w',
     'w                         w',
     'w                         w',
     'w                         w',
     'w                         w',
     'w                         w',
     'w                         w',
     'ws             p     f    w',
     'w                  wwwwwwww',
     'wwwwwwwwwwwwwwwwwwwwwwwwwww',
     ], [
        'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
        'w                               w',
        'w h                     b      Ew',
        'w                               w',
        'w                               w',
        'w                               w',
        'w                   k           w',
        'w                               w',
        'w                               w',
        'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
    ]

    , [

        'wwwwwwwwwwwwwwwwwwww',
        'wh     k w E       wwwwwwww',
        'w        w      g       www',
        'wwwwww   w              www',
        'ws     b wwwwwllllwwwwwwwww',
        'w        w                w',
        'ws       w           f    w',
        'w        w         wwwwwwww',
        'w                  ws    kw',
        'w                  w  d   w',
        'w        w  d      w      w',
        'w     p w w               w',
        'wwwwwwwwwwwwwwwwwwwwwwwwwww'
    ]
    , [
        'wwwwwwwwwwwwwwwwwwww',
        'wh       wE        wwwwwwww',
        'w        w      g       www',
        'wwwwww   w              www',
        'ws  b    wwwwwllllwwwwwwwww',
        'w        w                w',
        'ws       w     p     f    w',
        'w   b    w         wwwwwwww',
        'w            b     ws    kw',
        'w    p             w  w   w',
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
        'w  d               w  w   w',
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


def insert_enemy_randomly(enemy_count):
    global Map
    for i in range(enemy_count):
        possible_pos = False
        while not possible_pos:
            possible_pos = True
            x = random.randint(1, len(Map[0]) - 1)
            y = random.randint(1, len(Map[0][x]) - 1)
            if Map[0][x][y] != ' ':
                possible_pos = False
            else:
                Map[0][x] = Map[0][x][:y] + 'g' + Map[0][x][y + 1:]


insert_enemy_randomly(enemy_count)


def random_map():
    default_map = ['' for i in range(13)]
    for j in range(13):
        for i in range(28):
            letter = ' '
            if i == 0 or j == 0 or i == 27 or j == 12:
                letter = 'w'
            elif i == 1 and j == 1:
                letter = 'h'
            else:
                letter = random.randint(0, 100)
                if letter < 80:
                    letter = ' '
                # elif letter < 85:
                # letter = 'k'

                elif letter < 97:
                    letter = 'w'
                elif letter < 98:
                    letter = 'E'
                elif letter <= 100:
                    letter = 'g'

            default_map[j] += letter

    return default_map


#
# Map[0] = random_map()


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
def append_to_csv(filename, time, score, win):
    alg=''
    if enemy_intel:
        alg='minimax'
    else: alg = 'expectimax'
    fields = [ win, time, score, alg]
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def next_level():
    global map_surface, walls, enemies, spawners, items, gates, bullets, parents, score, before
    after = time.perf_counter()

    score += 1000
    append_to_csv('output.csv', after-before, score, True)
    walls = []
    gates = pygame.sprite.Group()
    items = pygame.sprite.Group()
    spawners = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    map_surface = draw_map()
    parents = mark_all_positions(exit_coords)


def draw_map():
    global hero, parents, exit_coords
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
                exit_coords = (j, i)
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


def check_wall(x, y, ignore_gates=False):
    for wall in walls:
        if wall.x // 32 == x and wall.y // 32 == y:
            return False
    if not ignore_gates:
        for gate in gates:
            if (gate.rect.x // 32 <= x <= (gate.rect.x + gate.rect.width) // 32) and (
                    gate.rect.y // 32 <= y <= (gate.rect.y + gate.rect.height) // 32) and keys == 0:
                return False
    return True


# def check_bullet(x, y):
#     # for bullet in bullets:
#     #     if bullet.type < 4 and bullet.rect.x // 32 - 1 <= x <= bullet.rect.x // 32 + 1 and bullet.rect.y // 32 - 1 <= y <= bullet.rect.y // 32 + 1:
#     #         return False
#
#     return True


def get_path(parents, point):
    path = []
    while point != [-1, -1]:
        path.append(point)
        point = parents[point[0]][point[1]][1]
    path.reverse()
    return path


def get_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def a_star(goal, start):
    global map_surface
    map_rect = map_surface.get_rect()
    answer = []
    queue = [[0, start]]
    visited = [[False for i in range(map_rect.height // 32)] for j in range(map_rect.width // 32)]
    parents = [[[] for i in range(map_rect.height // 32)] for j in range(map_rect.width // 32)]
    parents[start[0]][start[1]] = [0, [-1, -1]]
    while len(queue) > 0:

        # get the top element of the
        queue = sorted(queue)

        # print(queue)
        # for pr in visited:
        #     print(pr)
        p = queue.pop()
        if p[1] == goal:
            answer = get_path(parents, p[1])
            break
        if not visited[p[1][0]][p[1][1]]:

            if check_wall(p[1][0] + 1, p[1][1]):
                queue.append([(p[0] + 1 + get_dist([p[1][0] + 1, p[1][1]], goal)) * -1, [p[1][0] + 1, p[1][1]]])

                if len(parents[p[1][0] + 1][p[1][1]]) == 0:
                    parents[p[1][0] + 1][p[1][1]] = [parents[p[1][0]][p[1][1]][0] + 1, p[1]]

            if check_wall(p[1][0], p[1][1] + 1):
                queue.append([(p[0] + 1 + get_dist([p[1][0], p[1][1] + 1], goal)) * -1, [p[1][0], p[1][1] + 1]])
                if len(parents[p[1][0]][p[1][1] + 1]) == 0:
                    parents[p[1][0]][p[1][1] + 1] = [parents[p[1][0]][p[1][1]][0] + 1, p[1]]
            if check_wall(p[1][0] - 1, p[1][1]):
                queue.append([(p[0] + 1 + get_dist([p[1][0] - 1, p[1][1]], goal)) * -1, [p[1][0] - 1, p[1][1]]])
                if len(parents[p[1][0] - 1][p[1][1]]) == 0:
                    parents[p[1][0] - 1][p[1][1]] = [parents[p[1][0]][p[1][1]][0] + 1, p[1]]
            if check_wall(p[1][0], p[1][1] - 1):
                queue.append([(p[0] + 1 + get_dist([p[1][0], p[1][1] - 1], goal)) * -1, [p[1][0], p[1][1] - 1]])
                if len(parents[p[1][0]][p[1][1] - 1]) == 0:
                    parents[p[1][0]][p[1][1] - 1] = [parents[p[1][0]][p[1][1]][0] + 1, p[1]]
        visited[p[1][0]][p[1][1]] = True
    return answer


def uniform_cost_search(goal, start):
    global map_surface, count
    map_rect = map_surface.get_rect()
    answer = [[] for i in range(len(goal))]

    # create a priority queue
    queue = [[0, start]]

    # map to store visited node
    visited = [[False for i in range(map_rect.height // 32)] for j in range(map_rect.width // 32)]
    parents = [[[] for i in range(map_rect.height // 32)] for j in range(map_rect.width // 32)]
    parents[start[0]][start[1]] = [0, [-1, -1]]
    # count
    count = 0

    # while the queue is not empty
    while len(queue) > 0:

        # get the top element of the
        queue = sorted(queue)

        # print(queue)
        # for pr in visited:
        #     print(pr)
        p = queue.pop()

        # get the original value
        p[0] *= -1

        # check if the element is part of
        # the goal list
        if p[1] in goal:

            # get the position
            index = goal.index(p[1])

            # if a new goal is reached
            if len(answer[index]) == 0:
                count += 1
                answer[index] = get_path(parents, p[1])

            # if the cost is less
            if len(answer[index]) > p[0]:
                answer[index] = get_path(parents, p[1])

            # pop the element
            # queue.pop()

            queue = sorted(queue)
            if count == len(goal):
                return answer

        # check for the non visited nodes
        # which are adjacent to present node
        if not visited[p[1][0]][p[1][1]]:

            if check_wall(p[1][0] + 1, p[1][1]):
                if [(p[0] + 1) * -1, [p[1][0] + 1, p[1][1]]] not in queue:
                    queue.append([(p[0] + 1) * -1, [p[1][0] + 1, p[1][1]]])

                if len(parents[p[1][0] + 1][p[1][1]]) == 0 or parents[p[1][0] + 1][p[1][1]][0] > \
                        parents[p[1][0]][p[1][1]][0] + 1:
                    parents[p[1][0] + 1][p[1][1]] = [parents[p[1][0]][p[1][1]][0] + 1, p[1]]

            if check_wall(p[1][0], p[1][1] + 1):
                if [(p[0] + 1) * -1, [p[1][0], p[1][1] + 1]] not in queue:
                    queue.append([(p[0] + 1) * -1, [p[1][0], p[1][1] + 1]])
                if len(parents[p[1][0]][p[1][1] + 1]) == 0 or parents[p[1][0]][p[1][1] + 1][0] > \
                        parents[p[1][0]][p[1][1]][0] + 1:
                    parents[p[1][0]][p[1][1] + 1] = [parents[p[1][0]][p[1][1]][0] + 1, p[1]]
            if check_wall(p[1][0] - 1, p[1][1]):
                if [(p[0] + 1) * -1, [p[1][0] - 1, p[1][1]]] not in queue:
                    queue.append([(p[0] + 1) * -1, [p[1][0] - 1, p[1][1]]])
                if len(parents[p[1][0] - 1][p[1][1]]) == 0 or parents[p[1][0] - 1][p[1][1]][0] > \
                        parents[p[1][0]][p[1][1]][0] + 1:
                    parents[p[1][0] - 1][p[1][1]] = [parents[p[1][0]][p[1][1]][0] + 1, p[1]]
            if check_wall(p[1][0], p[1][1] - 1):
                if [(p[0] + 1) * -1, [p[1][0], p[1][1] - 1]] not in queue:
                    queue.append([(p[0] + 1) * -1, [p[1][0], p[1][1] - 1]])
                if len(parents[p[1][0]][p[1][1] - 1]) == 0 or parents[p[1][0]][p[1][1] - 1][0] > \
                        parents[p[1][0]][p[1][1]][0] + 1:
                    parents[p[1][0]][p[1][1] - 1] = [parents[p[1][0]][p[1][1]][0] + 1, p[1]]
        # mark as visited
        visited[p[1][0]][p[1][1]] = True

    return answer


def dfs(goal, start):
    global map_surface, count
    map_rect = map_surface.get_rect()
    answer = [[] for i in range(len(goal))]
    par = [[[] for i in range(map_rect.height // 32)] for j in range(map_rect.width // 32)]
    par[start[0]][start[1]] = [0, [-1, -1]]
    count = 0

    def dfs_recursive(parents, cur):
        global count
        if cur in goal:
            index = goal.index(cur)
            path = get_path(parents, cur)
            count += 1
            answer[index] = path

            # if the cost is less

        if len(goal) == count:
            return
            # pop the element

        if check_wall(cur[0] + 1, cur[1]) and len(parents[cur[0] + 1][cur[1]]) == 0:
            parents[cur[0] + 1][cur[1]] = [parents[cur[0]][cur[1]][0] + 1, cur]
            dfs_recursive(parents, [cur[0] + 1, cur[1]])
            # parents[cur[0] + 1][cur[1]] = []
        if check_wall(cur[0], cur[1] + 1) and len(parents[cur[0]][cur[1] + 1]) == 0:
            parents[cur[0]][cur[1] + 1] = [parents[cur[0]][cur[1]][0] + 1, cur]
            dfs_recursive(parents, [cur[0], cur[1] + 1])
            # parents[cur[0]][cur[1] + 1] = []
        if check_wall(cur[0] - 1, cur[1]) and len(parents[cur[0] - 1][cur[1]]) == 0:
            parents[cur[0] - 1][cur[1]] = [parents[cur[0]][cur[1]][0] + 1, cur]
            dfs_recursive(parents, [cur[0] - 1, cur[1]])
            # parents[cur[0] - 1][cur[1]] = []
        if check_wall(cur[0], cur[1] - 1) and len(parents[cur[0]][cur[1] - 1]) == 0:
            parents[cur[0]][cur[1] - 1] = [parents[cur[0]][cur[1]][0] + 1, cur]
            dfs_recursive(parents, [cur[0], cur[1] - 1])
            # parents[cur[0]][cur[1] - 1] = []

    dfs_recursive(par, start)
    return answer


def bfs(goal, start):
    global map_surface, count
    map_rect = map_surface.get_rect()
    answer = [[] for i in range(len(goal))]
    parents = [[[] for i in range(map_rect.height // 32)] for j in range(map_rect.width // 32)]
    parents[start[0]][start[1]] = [0, [-1, -1]]
    queue = [start]
    count = 0
    while len(queue) != 0:
        cur = queue.pop()
        if cur in goal:
            index = goal.index(cur)
            path = get_path(parents, cur)
            count += 1
            answer[index] = path

            # if the cost is less

        if len(goal) == count:
            return answer
        if check_wall(cur[0] + 1, cur[1]) and len(parents[cur[0] + 1][cur[1]]) == 0:
            parents[cur[0] + 1][cur[1]] = [parents[cur[0]][cur[1]][0] + 1, cur]
            queue.insert(0, [cur[0] + 1, cur[1]])
        if check_wall(cur[0], cur[1] + 1) and len(parents[cur[0]][cur[1] + 1]) == 0:
            parents[cur[0]][cur[1] + 1] = [parents[cur[0]][cur[1]][0] + 1, cur]
            queue.insert(0, [cur[0], cur[1] + 1])
        if check_wall(cur[0] - 1, cur[1]) and len(parents[cur[0] - 1][cur[1]]) == 0:
            parents[cur[0] - 1][cur[1]] = [parents[cur[0]][cur[1]][0] + 1, cur]
            queue.insert(0, [cur[0] - 1, cur[1]])
        if check_wall(cur[0], cur[1] - 1) and len(parents[cur[0]][cur[1] - 1]) == 0:
            parents[cur[0]][cur[1] - 1] = [parents[cur[0]][cur[1]][0] + 1, cur]
            queue.insert(0, [cur[0], cur[1] - 1])
    return answer


def mark_all_positions(start):
    global map_surface, max_dist
    map_rect = map_surface.get_rect()
    parents = [[[] for i in range(map_rect.height // 32)] for j in range(map_rect.width // 32)]
    parents[start[0]][start[1]] = [0, [-1, -1]]
    queue = [start]

    sides = [
        [0, 1],
        [1, 0],
        [0, -1],
        [-1, 0]
    ]
    while len(queue) != 0:
        cur = queue.pop()
        for side in sides:
            if check_wall(cur[0] + side[0], cur[1] + side[1], True) and len(
                    parents[cur[0] + side[0]][cur[1] + side[1]]) == 0:
                parents[cur[0] + side[0]][cur[1] + side[1]] = [parents[cur[0]][cur[1]][0] + 1, cur]
                queue.insert(0, [cur[0] + side[0], cur[1] + side[1]])
        # if check_wall(cur[0] + 1, cur[1], True) and len(parents[cur[0] + 1][cur[1]]) == 0:
        #     parents[cur[0] + 1][cur[1]] = [parents[cur[0]][cur[1]][0] + 1, cur]
        #     queue.insert(0, [cur[0] + 1, cur[1]])
        # if check_wall(cur[0], cur[1] + 1, True) and len(parents[cur[0]][cur[1] + 1]) == 0:
        #     parents[cur[0]][cur[1] + 1] = [parents[cur[0]][cur[1]][0] + 1, cur]
        #     queue.insert(0, [cur[0], cur[1] + 1])
        # if check_wall(cur[0] - 1, cur[1], True) and len(parents[cur[0] - 1][cur[1]]) == 0:
        #     parents[cur[0] - 1][cur[1]] = [parents[cur[0]][cur[1]][0] + 1, cur]
        #     queue.insert(0, [cur[0] - 1, cur[1]])
        # if check_wall(cur[0], cur[1] - 1, True) and len(parents[cur[0]][cur[1] - 1]) == 0:
        #     parents[cur[0]][cur[1] - 1] = [parents[cur[0]][cur[1]][0] + 1, cur]
        #     queue.insert(0, [cur[0], cur[1] - 1])
        if max_dist < parents[cur[0]][cur[1]][0] + 1:
            max_dist = parents[cur[0]][cur[1]][0] + 1
    return parents


def collide(rect1, rect2):
    if rect2.colliderect(rect1):

        if 0 <= rect2.x - rect1.x + 32 < hero_type + 4:
            rect1.x = rect2.x + 32
        elif 0 <= rect1.x - rect2.x + 32 < hero_type + 4:
            rect1.x = rect2.x - 32
        if 0 <= rect2.y - rect1.y + 32 < hero_type + 4:
            rect1.y = rect2.y + 32
        elif 0 <= rect1.y - rect2.y + 32 < hero_type + 4:
            rect1.y = rect2.y - 32


def update():
    global keys, potions, score, running, invulnerability, level, map_surface, minimax_moves, nearest_enemy, turns, random_moves
    score -= 1
    screen.blit(map_surface, (0, 0))
    finding_items = []
    paths = []
    if turns > 1 or len(minimax_moves) <2:
        tree = None
        nearest_enemy = find_nearest_enemy([hero.rect.x // 32, hero.rect.y // 32])
        if nearest_enemy:
            tree = generate_minimax_tree_recurs(Node(hero.rect.x // 32, hero.rect.y // 32),
                                                Node(nearest_enemy.rect.x // 32, nearest_enemy.rect.y // 32), 0)
        else:
            tree = generate_minimax_tree_recurs(Node(hero.rect.x // 32, hero.rect.y // 32),
                                                Node(1, 1), 0)
        if enemy_intel:
            minimax(tree, 0, -math.inf, math.inf, True)
        else:
            expectimax(tree, 0, True)
            sides = [
                [0, 1],
                [1, 0],
                [0, -1],
                [-1, 0]
            ]
            for enemy in enemies:
                random_moves[enemy] = [sides[random.randint(0, 3)], sides[random.randint(0, 3)]]

        minimax_moves = find_moves_from_tree(tree, 0)
        minimax_moves.pop(0)
        print(minimax_moves)
        turns = 0
    # print(a)
    for item in items:
        if item.type == 5 or item.type == 12:
            finding_items.append([item.rect.x // 32, item.rect.y // 32])

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

                if level > 1:
                    running = False
                else:
                    next_level()
            item.kill()
    if finding_type == 0:
        before = time.perf_counter()
        paths = uniform_cost_search(finding_items,
                                    [hero.rect.x // 32, hero.rect.y // 32])
        after = time.perf_counter()
        if after - before < best_time[0]:
            best_time[0] = after - before
    elif finding_type == 1:
        before = time.perf_counter()
        paths = dfs(finding_items, [hero.rect.x // 32, hero.rect.y // 32])
        after = time.perf_counter()
        if after - before < best_time[1]:
            best_time[1] = after - before
    elif finding_type == 2:
        before = time.perf_counter()
        paths = bfs(finding_items, [hero.rect.x // 32, hero.rect.y // 32])
        after = time.perf_counter()
        if after - before < best_time[2]:
            best_time[2] = after - before
    elif finding_type == 3:
        for fi in finding_items:
            paths.append(a_star(fi, [hero.rect.x // 32, hero.rect.y // 32]))

    # for path in paths:
    #     for point in path:
    #         pygame.draw.rect(screen, (64, 128, 255), (point[0] * 32 + 4, point[1] * 32 + 4, 24, 24))

    # paths = [path for path in paths if path]
    if (len(minimax_moves) > turns * 2):

        if hero.rect.x < minimax_moves[turns * 2][0] * 32:
            hero.setXChange(1)
        elif hero.rect.x > minimax_moves[turns * 2][0] * 32:
            hero.setXChange(-1)
        else:
            hero.setXChange(0)
        if hero.rect.y < minimax_moves[turns * 2][1] * 32:
            hero.setYChange(1)
        elif hero.rect.y > minimax_moves[turns * 2][1] * 32:
            hero.setYChange(-1)
        else:
            hero.setYChange(0)
        if hero.rect.x // 32 == minimax_moves[turns * 2][0] and hero.rect.y // 32 == minimax_moves[turns * 2][1]:
            hero.setYChange(0)
            hero.setXChange(0)
            # parents[minimax_moves[turns * 2][0]][minimax_moves[turns * 2][1]][0] = max_dist
            turns += 1

    else:
        hero.setYChange(0)
        hero.setXChange(0)
    randint = random.randint(0, 100)
    if randint > 96:
        bullet = hero.shoot()
        if bullet:
            bullets.add(hero.shoot())
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
        if enemy_intel:
            if enemy == nearest_enemy:

                if len(minimax_moves) > 1 + turns * 2:

                    if enemy.rect.x < minimax_moves[1 + turns * 2][0] * 32:
                        enemy.setXChange(1)
                    elif enemy.rect.x > minimax_moves[1 + turns * 2][0] * 32:
                        enemy.setXChange(-1)
                    else:
                        enemy.setXChange(0)
                    if enemy.rect.y < minimax_moves[1 + turns * 2][1] * 32:
                        enemy.setYChange(1)
                    elif enemy.rect.y > minimax_moves[1 + turns * 2][1] * 32:
                        enemy.setYChange(-1)
                    else:
                        enemy.setYChange(0)

            else:
                path = a_star([hero.rect.centerx // 32, hero.rect.centery // 32],
                              [enemy.rect.centerx // 32, enemy.rect.centery // 32])
                # path = []
                # for point in path:
                #     pygame.draw.rect(screen, (255, 128, 255), (point[0] * 32 + 4, point[1] * 32 + 4, 24, 24))

                if len(path) > 2:
                    if enemy.rect.x < path[1][0] * 32 - 1:
                        enemy.setXChange(1)
                    elif enemy.rect.x > path[1][0] * 32 + 1:
                        enemy.setXChange(-1)
                    else:
                        enemy.setXChange(0)
                    if enemy.rect.y < path[1][1] * 32 - 1:
                        enemy.setYChange(1)
                    elif enemy.rect.y > path[1][1] * 32 + 1:
                        enemy.setYChange(-1)
                    else:
                        enemy.setYChange(0)
                else:
                    enemy.setYChange(0)
                    enemy.setXChange(0)
            direction_move = [
                [1, 0], [-1, 0], [0, 1], [0, -1], [-1, 0], [1, 0], [0, -1], [1, 0]
            ]
            for bullet in bullets:
                if bullet.type < 4:
                    if get_dist([bullet.rect.x // 32, bullet.rect.y // 32],
                                [enemy.rect.x // 32, enemy.rect.y // 32]) < 3:
                        x, y = direction_move[bullet.direction]
                        enemy.setXChange(x)
                        enemy.setYChange(y)
        else:
            try:
                move = random_moves[enemy]
                if (len(move) > turns):
                    enemy.setXChange(move[turns][0])
                    enemy.setYChange(move[turns][1])
            except:
                print('')


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
    screen.blit(f.render('Score:' + str(score), 1, (255, 255, 255)), (900, 16))
    screen.blit(f.render('Potions:' + str(potions), 1, (255, 255, 255)), (900, 48))
    screen.blit(f.render('HP:' + str(hero.hp), 1, (255, 255, 255)), (900, 80))
    screen.blit(f.render('Keys:' + str(keys), 1, (255, 255, 255)), (900, 112))
    screen.blit(f.render('Finding alg:' + str(finding_type), 1, (255, 255, 255)), (900, 144))
    for i in range(3):
        screen.blit(f.render('Finding alg time ' + str(i) + ':' + str(best_time[i]), 1, (255, 255, 255)),
                    (16, 400 + 32 * (i + 1)))
    if invulnerability > 0:
        invulnerability -= 1


def find_nearest_enemy(position):
    global enemies
    nearest_enemy_path = None
    nearest_enemy = None
    for enemy in enemies:
        path = a_star(position, [enemy.rect.centerx // 32, enemy.rect.centery // 32])
        if nearest_enemy_path is None or len(path) < len(nearest_enemy_path):
            nearest_enemy = enemy
            nearest_enemy_path = path
    return nearest_enemy


def find_moves_from_tree(node: Node, depth):
    # move_node = Node(node.x, node.y, node.get_score())
    move_node = [[node.x, node.y]]
    for neighbor in node.get_neighbors():
        if ((enemy_intel or depth % 2 == 0) and math.fabs(neighbor.get_score() - node.get_score()) < 0.1) or (
                not enemy_intel and depth % 2 == 1 and \
                neighbor.x == random_moves[nearest_enemy][depth // 2][0] + nearest_enemy.rect.x // 32 and \
                neighbor.y == random_moves[nearest_enemy][depth // 2][1] + nearest_enemy.rect.y // 32):
            neighbor_node = find_moves_from_tree(neighbor, depth + 1)
            move_node = move_node + neighbor_node
            break

    return move_node


def expectimax(node, depth, is_max_player):
    if depth > 3:
        return node.get_score()
    if is_max_player:
        best_val = -math.inf
        for neighbor in node.get_neighbors():
            value = expectimax(neighbor, depth + 1, False)
            if value > best_val:
                best_val = value

        node.set_score(best_val)
        return best_val

    else:
        value_sum = 0
        for neighbor in node.get_neighbors():
            value = expectimax(neighbor, depth + 1, True)
            value_sum += value
        best_val = value_sum / len(node.get_neighbors())
        node.set_score(best_val)
        return best_val


def minimax(node, depth, alpha, beta, is_max_player):
    if depth > 3:
        return node.get_score()
    if is_max_player:
        best_val = -math.inf
        for neighbor in node.get_neighbors():
            value = minimax(neighbor, depth + 1, alpha, beta, False)
            if value > best_val:
                best_val = value
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        node.set_score(best_val)
        return best_val

    else:
        best_val = math.inf
        for neighbor in node.get_neighbors():
            value = minimax(neighbor, depth + 1, alpha, beta, True)
            if value < best_val:
                best_val = value
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        node.set_score(best_val)
        return best_val


def evaluate(max_player, min_player, temp_score):
    global parents, exit_coords
    path = a_star([max_player.x, max_player.y], [min_player.x, min_player.y])

    # exit_path = a_star([max_player.x, max_player.y], exit_coords)
    return ((max_dist - parents[max_player.x][max_player.y][0]) / max_dist * 1000 - (
            max_dist - len(path)) / max_dist * 700 + score - 20 + temp_score)
    # + (max_dist-len(exit_path))/max_dist * 5000)


def generate_minimax_tree_recurs(max_player: Node, min_player: Node, depth, visited=None, temp_score=0):
    visited = visited or [[max_player.x, max_player.y], [min_player.x, min_player.y]]
    if depth > 3:
        min_player.set_score(evaluate(max_player, min_player, temp_score))
        return min_player
    sides = [
        [0, 1],
        [1, 0],
        [0, -1],
        [-1, 0]
    ]
    if depth % 2 == 0:
        for side in sides:
            x = max_player.x + side[0]
            y = max_player.y + side[1]
            if (x < 0 or y < 0 or x >= len(parents) or len(parents[x]) <= y) or not check_wall(x, y, True) \
                    or [x, y] == visited[0]:
                continue
            for item in items:
                if [x, y] == [item.rect.x // 32, item.rect.y // 32]:
                    if 6 < item.type < 10:
                        temp_score += 100
                    elif item.type == 12:
                        temp_score += 5000
                    elif item.type == 5:
                        temp_score += 500
            for enemy in enemies:
                if [x, y] == [enemy.rect.x // 32, enemy.rect.y // 32]:
                    temp_score -= 1000
            neighbor = generate_minimax_tree_recurs(Node(x, y), min_player, depth + 1, visited, temp_score)
            min_player.add_neighbor(neighbor)
        return min_player
    else:
        for side in sides:
            x = min_player.x + side[0]
            y = min_player.y + side[1]
            if (x < 0 or y < 0 or x >= len(parents) or len(parents[x]) <= y) or not check_wall(x, y, True) \
                    or [x, y] == visited[1]:
                continue
            for item in items:
                if [x, y] == [item.rect.x // 32, item.rect.y // 32]:
                    if 6 < item.type < 10:
                        temp_score += 100
                    elif item.type == 12:
                        temp_score += 5000
            for enemy in enemies:
                if [x, y] == [enemy.rect.x // 32, enemy.rect.y // 32]:
                    temp_score -= 1000
            neighbor = generate_minimax_tree_recurs(max_player, Node(x, y), depth + 1, visited, temp_score)
            max_player.add_neighbor(neighbor)
        return max_player


map_surface = draw_map()
parents = mark_all_positions(exit_coords)
before = time.perf_counter()
while running:
    screen.fill((0, 0, 0))
    if score< -400:
        after = time.perf_counter()
        append_to_csv('output.csv', after-before, score, False)
        break
    if hero.hp > 0:
        update()
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
                if event.key == pygame.K_z:
                    finding_type += 1
                    if finding_type > 3:
                        finding_type = 0
                # if event.key == pygame.K_SPACE:
                #     bullets.add(hero.shoot())
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



    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(f.render('Score:' + str(score), 1, (255, 255, 255)), (160, 160))
    clock.tick(fps)
    pygame.display.update()
