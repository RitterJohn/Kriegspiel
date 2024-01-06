import random
import pygame
from pygame.locals import *
import numpy as np

# Цвета
C1 = (0, 250, 50)
C2 = (0, 250, 250)
White = (250, 250, 250)
BLACK = (0, 0, 0)
Gray = (200, 200, 200)
Gray2 = (50, 50, 50)

size = 1520, 800
FPS = 100

pygame.mixer.pre_init(44100, -16, 1, 4096)
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Krieg")
clock = pygame.time.Clock()
sound0 = pygame.mixer.Sound('resources\\0.ogg')
sound0.set_volume(0.2)
sound02 = pygame.mixer.Sound('resources\\0.ogg')
sound02.set_volume(0.1)

go_check = False # для проверки движения
player1 = True # для смены хода
canon_select = False # для проверки, выбран ли отряд артиллерии

# словари для соотнесения отрядов и их номеров
dict_0 = {} # для игрока, ход которого в данный момент
dict_1 = {} # для первого игрока
dict_2 = {} # для второго игрока

class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.left = x
        self.center = (x, y)
        self.run_speed = (0, -1)
        self.direction = 0
        self.dist = 0
        self.max_dist = 100
        self.angle = 0
        self.fire = False
        self.time = random.randint(0, 200)
        self.comand = 0
        self.x_d = x
        self.y_d = y

    def shot(self):
        bullet = Bullet(self.rect.left + 10 * np.sign(np.sin(self.angle / 180 * np.pi)), self.rect.top - 10 * np.sign(np.cos(self.angle / 180 * np.pi)), 200, 10, self.angle)
        all_sprites.add(bullet)
        bullets.add(bullet)
        smoke_add(self.rect.left, self.rect.bottom, 1, 4, 4)

    def go(self):
        self.x_d += np.sin(self.angle / 180 * np.pi)
        self.y_d -= np.cos(self.angle / 180 * np.pi)
        self.rect.center = (self.x_d, self.y_d)
        self.dist += abs(np.sign(np.sin(self.angle / 180 * np.pi) * np.cos(self.angle / 180 * np.pi)) * 0.41) + 1

    def update(self):
        if (self.fire == True):
            if (pygame.time.get_ticks() - self.comand >= self.time):
                self.shot()
                self.time = random.randint(0, 200)
                self.fire = False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dist, alpha, dir):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.image.fill(White)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.left = x
        self.speed = (1, 1)
        self.max = random.randint(50, dist)
        self.angle = np.pi * (random.randint(-alpha, alpha)) / 180 + np.pi * (dir) / 180
        self.way = 0
        self.dist = 0
        self.x_d = x
        self.y_d = y

    def update (self):
        self.x_d += np.sin(self.angle)
        self.y_d -= np.cos(self.angle)
        self.rect.center = (self.x_d, self.y_d)
        self.way += 1
        if self.way >= self.max:
            self.kill()

class Core(pygame.sprite.Sprite):
    def __init__(self, x, y, xz, yz):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill(White)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.left = x
        self.speed = (0, -1)
        self.max = random.randint(300, 800)
        self.angle = np.pi * random.randint(-5, 5) / 180
        self.way = 0
        self.dist = 0
        self.xz = xz
        self.yz = yz
        # self.s = False
        self.a = np.tan(self.angle) + (self.xz - self.rect.left) / (-self.yz + self.rect.bottom)

    def update (self):
        self.rect.bottom += self.speed[1]
        self.way += abs(self.speed[1])
        if (abs(self.a) > 0.01):
            self.dist = round(1 / self.a)
            if (self.way % abs(self.dist)) == 0:
                self.rect.left += np.sign(self.a)
        if self.way >= self.max or self.rect.bottom < 0:
            self.kill()

class Smoke(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((random.randint(1, 3), (random.randint(1, 3))))
        self.image.fill(Gray)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.left = x
        self.speed = (0.1, 0.05)
        self.x = x
        self.y = y
        self.x_d = 0
        self.y_d = 0
        self.max = random.randint(100, 250)
        self.way = 0
        self.dist = 0

    def update (self):
        self.x_d += self.speed[0]
        self.y_d += self.speed[1]
        self.rect.left += self.x_d // 1
        self.rect.bottom += self.y_d // 1
        if self.x_d >= 1:
            self.x_d = 0
        if self.y_d >= 1:
            self.y_d = 0
        self.way += 1
        if self.way >= self.max:
            self.kill()

class Canon(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.move_down = False
        self.move_up = False
        self.way_down = 0
        self.way = 0
        self.fire = False
        self.grapeshot_fire = False
        self.time = random.randint(0, 500)
        self.comand = 0
        self.down = False

    def core_shot(self, zx, zy):
        a = (zx - self.rect.left) / (-zy + self.rect.top)
        if (abs(a) < 0.43):
            core1 = Core(self.rect.left + 3, self.rect.top - 2, zx, zy)
            sound0.play(maxtime=2000)
            all_sprites.add(core1)
            cores.add(core1)
            smoke_add(self.rect.left + 3, self.rect.top + 4, 4, 11, 60)
            self.move_down = True
            self.move_up = False

    def update(self):
        if(self.way_down < 4 and self.move_down == True):
            self.rect.top += 1
            self.way_down += 1
        if (self.way_down == 4 and self.move_down == True):
            self.move_down = False
            self.move_up = True
        if(self.way_down > 0 and self.move_up == True):
            self.way += 0.02
            if (self.way >= 1):
                self.rect.top -= 1
                self.way = 0
            self.way_down -= 0.02
        if (self.way_down <= 0 and self.move_up == True):
            self.move_up = False
            self.way = 0
            self.way_down = 0
        if (self.fire == True):
            if (pygame.time.get_ticks() - self.comand >= self.time):
                self.core_shot(ziel[0], ziel[1])
                self.time = random.randint(0, 500)
                self.fire = False
        if (self.grapeshot_fire == True):
            if (pygame.time.get_ticks() - self.comand >= self.time):
                self.grapeshot()
                self.time = random.randint(0, 500)
                self.grapeshot_fire = False

    def grapeshot(self):
        for i in range(50):
            bul = Bullet(self.rect.left + 3, random.randint(self.rect.top - 4, self.rect.top), 250, 8, 0)
            all_sprites.add(bul)
            bullets.add(bul)
        sound0.play(maxtime=2000)
        smoke_add(self.rect.left + 3, self.rect.top + 4, 4, 11, 60)
        self.move_down = True
        self.move_up = False

# функция для создания дыма после выстрела
def smoke_add(x, y, x_r, y_r, n):
    for i in range(n):
        u = Smoke(random.randint(x - x_r, x + x_r), random.randint(y - y_r, y))
        all_sprites.add(u)

# функция для перестроения отряда (заполнение мест убитых солдат)
def new_position(a):
    i = 0
    for unit in a:
        if (i == 0):
            x = unit.rect.left
            y = unit.rect.bottom
        alpha = unit.angle / 180 * np.pi
        if (unit.angle % 90 == 0):
            unit.rect.left = x + 4 * (i % 30) * np.cos(alpha) - 4 * (i // 30) * np.sin(alpha)
            unit.rect.bottom = y + 4 * (i // 30) * np.cos(alpha) + 4 * (i % 30) * np.sin(alpha)
        else:
            betta = (unit.angle + 90) / 180 * np.pi
            unit.rect.left = x + np.sign(np.cos(alpha)) * 3 * (i % 30) + np.sign(np.cos(betta)) * (i // 30) * 3
            unit.rect.bottom = y + np.sign(np.sin(alpha)) * 3 * (i % 30) + np.sign(np.sin(betta)) * (i // 30) * 3
        i += 1

# функция для добавления расчёта к орудию
def artillery(x, y, group, C):

    un1 = Unit(x + 13, y + 8, C)
    un2 = Unit(x + 11, y + 11, C)
    un3 = Unit(x + 12, y - 2, C)
    un4 = Unit(x - 5, y + 1, C)
    un5 = Unit(x - 4, y + 14, C)
    un6 = Unit(x - 1, y + 24, C)
    units.add(un1, un2, un3, un4, un5, un6)
    all_sprites.add(un1, un2, un3, un4, un5, un6)
    group.add(un1, un2, un3, un4, un5, un6)

# функция для создания отряда пехоты
def add_unit(a, x, y, C):
    units_list.append(a)
    for i in range(90):
        un = Unit(x + 4 * ((i) % 30), y + 4 * (i // 30 + 1), C)
        all_sprites.add(un)
        a.add(un)
        units.add(un)

# функция для правого поворота отряда
def povorot(a):
    i = 0
    for u in a:
        alpha = (u.angle + 1) / 180 * np.pi
        if (abs(np.cos(alpha)) > abs(np.cos(np.pi / 4))):
            u.rect.bottom -= np.sign(np.cos(alpha)) * (np.sign(np.tan(alpha) * np.tan(alpha + np.pi/4)) * abs((29 - i) // 30) + np.sign(np.tan(alpha) * np.tan(alpha + np.pi/4)) * 6 + ((29 - i) % 30) * 3)
            u.rect.left += np.sign(np.sin(alpha)) * (np.sign(np.tan(alpha) * np.tan(alpha + np.pi/4)) * 6 + np.sign(np.tan(alpha) * np.tan(alpha + np.pi/4)) * ((29 - i) // 30) * 3 + ((29 - i) % 30))
        else:
            u.rect.bottom -= np.sign(np.cos(alpha)) * (np.sign(np.tan(alpha) * np.tan(alpha + np.pi/4)) * 6 + np.sign(np.tan(alpha) * np.tan(alpha + np.pi/4)) * ((29 - i) // 30) * 3 + ((29 - i) % 30))
            u.rect.left += np.sign(np.sin(alpha)) * (np.sign(np.tan(alpha) * np.tan(alpha + np.pi/4)) * abs((29 - i) // 30) - np.sign(np.tan(alpha) * np.tan(alpha + np.pi/4)) * 6 + ((29 - i) % 30) * 3)
        u.angle = (u.angle + 45) % 360
        i += 1

# функция для левого поворота отряда
def left_povorot(a):
    i = 0
    for u in a:
        alpha = (u.angle - 1) / 180 * np.pi
        b = np.sign(np.tan(alpha) * np.tan(alpha - np.pi/4))
        if (abs(np.cos(alpha)) > abs(np.cos(np.pi / 4))):
            u.rect.bottom -= np.sign(np.cos(alpha)) * (b * abs((i) // 30) + b * 6 + ((i) % 30) * 3)
            u.rect.left -= np.sign(np.sin(alpha)) * (b * 6 + b * ((i) // 30) * 3 - ((i) % 30))
        else:
            u.rect.bottom -= np.sign(np.cos(alpha)) * (b * 6 - b * ((i) // 30) * 3 + ((i) % 30))
            u.rect.left -= np.sign(np.sin(alpha)) * (-b * abs((i) // 30) - b * 6 - ((i) % 30) * 3)
        u.angle = (u.angle - 45) % 360
        i += 1

running = True

units_list = []
act_list = [0, 0, 0, 0]
line_list = [(0, 0), (0, 0), (0, 0)]

all_sprites = pygame.sprite.Group()
units = pygame.sprite.Group()
units1 = pygame.sprite.Group()
units2 = pygame.sprite.Group()
units3 = pygame.sprite.Group()
units4 = pygame.sprite.Group()
units5 = pygame.sprite.Group()
units6 = pygame.sprite.Group()
batery1 = pygame.sprite.Group()
batery2 = pygame.sprite.Group()
canons1 = pygame.sprite.Group()
canons2 = pygame.sprite.Group()
bullets = pygame.sprite.Group()
cores = pygame.sprite.Group()
canons = pygame.sprite.Group()

# создание отрядов пехоты первого игрока
add_unit(units1, 450, 600, C1)
dict_1[0] = units1
add_unit(units2, 700, 600, C1)
dict_1[1] = units2
add_unit(units3, 850, 600, C1)
dict_1[2] = units3

# создание отрядов пехоты второго игрока
add_unit(units4, 550, 600, C2)
dict_2[0] = units4
add_unit(units5, 800, 600, C2)
dict_2[1] = units5
add_unit(units6, 950, 600, C2)
dict_2[2] = units6

for a in dict_2.values():
    for unit in a:
        unit.rect.left = size[0] - unit.rect.left
        unit.rect.bottom = size[1] - unit.rect.bottom

selected_unit = units1
dict_0 = dict_1
dict_n = dict_2

canon1 = Canon(600, 600, 'resources/canon.png')
all_sprites.add(canon1)
canons.add(canon1)
canons1.add(canon1)
canon2 = Canon(635, 600, 'resources/canon.png')
all_sprites.add(canon2)
canons.add(canon2)
canons1.add(canon2)
canon3 = Canon(670, 600, 'resources/canon.png')
all_sprites.add(canon3)
canons.add(canon3)
canons1.add(canon3)

canon4 = Canon(750, 185, 'resources/canon2.png')
all_sprites.add(canon4)
canons.add(canon4)
canons2.add(canon4)
canon5 = Canon(785, 185, 'resources/canon2.png')
all_sprites.add(canon5)
canons.add(canon5)
canons2.add(canon5)
canon6 = Canon(820, 185, 'resources/canon2.png')
all_sprites.add(canon6)
canons.add(canon6)
canons2.add(canon6)
canon4.down = True
canon5.down = True
canon6.down = True

artillery(600, 600, batery1, C1)
artillery(635, 600, batery1, C1)
artillery(670, 600, batery1, C1)

artillery(763, 600, batery2, C2)
artillery(728, 600, batery2, C2)
artillery(693, 600, batery2, C2)

selected_canons = canons1

c_count = 0
for canon in selected_canons:
    line_list[c_count] = (canon.rect.left + 3, canon.rect.top + 2)
    c_count += 1

for unit in batery2:
    unit.rect.left = size[0] - unit.rect.left
    unit.rect.bottom = size[1] - unit.rect.bottom

score_font = pygame.font.SysFont('consolas', 14)
score_text = []
action_text = score_font.render(str(act_list), True, (White))
for unit in units_list:
    score_text.append(score_font.render(f'{len(unit.sprites())}', True, unit.sprites()[0].color))

while running:

    clock.tick(FPS)
    k = list(dict_0.keys())[list(dict_0.values()).index(selected_unit)]

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # Выстрел из пушки
        elif event.type == MOUSEBUTTONDOWN and canon_select == True and act_list[3] == 0:
            ziel = event.pos
            for canon in selected_canons:
                canon.fire = True
                canon.comand = pygame.time.get_ticks()
            canon_select = False
            act_list[3] = 1
        elif event.type == KEYDOWN:
            # Смена хода
            if event.key == K_RETURN:
                for unit in dict_0.values():
                    new_position(unit)
                for sprite in all_sprites:
                    sprite.rect.left = size[0] - sprite.rect.left
                    sprite.rect.bottom = size[1] - sprite.rect.bottom
                for unit in dict_n.values():
                    new_position(unit)
                for canon in canons:
                    if canon.down == False:
                        canon.image = pygame.image.load('resources/canon2.png')
                        canon.down = True
                    else:
                        canon.image = pygame.image.load('resources/canon.png')
                        canon.down = False
                    canon.rect.left -= 8
                    canon.rect.bottom += 15
                if (player1 == True):
                    dict_0 = dict_2
                    dict_n = dict_1
                    selected_unit = units4
                    selected_canons = canons2
                    player1 = False
                else:
                    dict_0 = dict_1
                    dict_n = dict_2
                    selected_unit = units1
                    selected_canons = canons1
                    player1 = True
                for a in dict_0.values():
                    for u in a:
                        u.dist = 0
                act_list = [0, 0, 0, 0]
                line_list = []
                for canon in selected_canons:
                    line_list.append((canon.rect.left + 3, canon.rect.top + 2))
            # Выбор отряда
            elif event.key == K_1:
                selected_unit = dict_0[0]
            elif event.key == K_2:
                selected_unit = dict_0[1]
            elif event.key == K_3:
                selected_unit = dict_0[2]
            elif event.key == K_4 and act_list[3] == 0:
                canon_select = True
            # Выстрел отряда пехоты
            elif event.key == K_f and act_list[k] == 0:
                sound02.play(maxtime=2000)
                j = 0
                for u in selected_unit:
                    if random.randint(0, 100) >= 15 and j < 60:
                        u.fire = True
                        u.comand = pygame.time.get_ticks()
                        j += 1
                act_list[k] = 1
            # Выстрел картечью
            elif event.key == K_g and canon_select == True and act_list[3] == 0:
                for canon in selected_canons:
                    canon.comand = pygame.time.get_ticks()
                    canon.grapeshot_fire = True
                canon_select = False
                act_list[3] = 1
            elif event.key == K_w and act_list[k] != 1:
                go_check = True
            elif event.key == K_e and act_list[k] != 1:
                i_un = 0
                for u in selected_unit:
                    if u.dist <= 75 and i_un == 0:
                        povorot(selected_unit)
                        act_list[k] = 0.5
                        u.dist += 25
                    elif u.dist <= 75:
                        u.dist += 25
                    i_un += 1
            elif event.key == K_q:
                i_un = 0
                for u in selected_unit:
                    if u.dist <= 75 and i_un == 0:
                        left_povorot(selected_unit)
                        act_list[k] = 0.5
                        u.dist += 25
                    elif u.dist <= 75:
                        u.dist += 25
                    i_un += 1
        elif event.type == KEYUP:
            if event.key == K_w:
                go_check = False

    all_sprites.update()

    if go_check == True:
        act_list[k] = 0.5
        for u in selected_unit:
            if (u.dist < u.max_dist):
                u.x_d, u.y_d = u.rect.center
                u.go()
            else:
                go_check = False
                act_list[k] = 1

    # Проверка столкновений:
    pygame.sprite.groupcollide(units, bullets, True, True)
    pygame.sprite.groupcollide(units, cores, True, False)
    pygame.sprite.groupcollide(canons, cores, True, False)

    for i in range(len(units_list)):
        if (len(units_list[i].sprites())) > 0:
            score_text[i] = score_font.render(f'{len(units_list[i].sprites())}', True, units_list[i].sprites()[0].color)

    for group in units_list:
        if len(group) < 20:
            for unit in group:
                unit.image.fill(White)
                unit.rect = unit.rect.move (unit.run_speed)

                if unit.rect.top <= 0 or unit.rect.left <= 0 or unit.rect.right >= size[0]:
                    unit.kill()

    p1_count = len(units1) + len(units2) + len(units3)
    p2_count = len(units4) + len(units5) + len(units6)

    if (p2_count < 20):
        running = False
        print('Россия победила!')
    if (p1_count < 20):
        running = False
        print('Франция победила!')

    screen.fill(BLACK)
    if (canon_select == True):
        for line in line_list:
            pygame.draw.line(screen, Gray2, line, (line[0] - 0.43 * line[1], 0), 1)
            pygame.draw.line(screen, Gray2, line, (line[0] + 0.43 * line[1], 0), 1)
    all_sprites.draw(screen)
    for i in range(len(units_list)):
        if (len(units_list[i].sprites())) > 0:
            screen.blit(score_text[i], (units_list[i].sprites()[0].rect.left, units_list[i].sprites()[0].rect.bottom - 30))
    action_text = score_font.render(str(act_list), True, (White))
    p1_text = score_font.render(str(p1_count), True, (C1))
    p2_text = score_font.render(str(p2_count), True, (C2))
    screen.blit(action_text, (30, 20))
    screen.blit(p1_text, (1400, 20))
    screen.blit(p2_text, (1400, 40))
    pygame.display.update()

pygame.time.delay(500)
pygame.quit()