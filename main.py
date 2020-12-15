import pygame
import math
from random import *
import time
import numpy as np

W = 1024
H = 720
screen = pygame.display.set_mode((W, H))

FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (162, 82, 45)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
pygame.init()
clock = pygame.time.Clock()


class Bars(pygame.sprite.Sprite):
    def __init__(self, bar_type, y):
        self.type = bar_type
        self.amount = 0
        if self.type == "health":
            self.color = RED
        elif self.type == "boost":
            self.color = BLUE

        super().__init__()
        self.image = pygame.Surface([300, 100], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = [160, y]

    def update(self):
        if self.type == "health":
            self.amount = worm.health
        elif self.type == "boost":
            if worm.boost_end > time.time():
                self.amount = (worm.boost_end - time.time()) / worm.boost_time
            else:
                self.amount = 0

        pygame.draw.rect(self.image, WHITE, (0, 0, 300, 30), border_radius=15)
        pygame.draw.rect(self.image, self.color, (5, 5, 290 * self.amount, 20), border_radius=10)
        pygame.draw.rect(self.image, BLACK, (0, 0, 300, 30), width=5, border_radius=15)


class Map:
    def __init__(self, width, height):
        self.head = list_of_segments[0]  # Worm head
        self.background = pygame.image.load("bg.png")
        self.rock_bg = pygame.image.load("rock.png")
        self.grass_bg = pygame.image.load("grass.png")
        self.width = width
        self.height = height
        self.bg_width = self.background.get_rect().width
        self.bg_height = self.background.get_rect().height

    def update_bg(self):
        # Moving background
        rel_x = W - self.head.x_lab % self.bg_width
        rel_y = H - self.head.y_lab % self.bg_height
        screen.blit(self.background, (rel_x - self.bg_width,
                                      rel_y - self.bg_height))
        if rel_x < W:
            if self.head.x_lab > self.width/2 - self.bg_width:
                screen.blit(self.rock_bg, (rel_x, rel_y - self.bg_height))
            else:
                screen.blit(self.background, (rel_x, rel_y - self.bg_height))
        if rel_y < H:
            if self.head.y_lab > self.height/2 - self.bg_height and rel_y > 0:
                screen.blit(self.rock_bg, (rel_x - self.bg_width, rel_y))
            else:
                screen.blit(self.background, (rel_x - self.bg_width, rel_y))
        if rel_x < W and rel_y < H:
            if self.head.x_lab > self.width/2 - self.bg_width or \
                    (self.head.y_lab > self.height/2 - self.bg_height and rel_y > 0):
                screen.blit(self.rock_bg, (rel_x, rel_y))
            else:
                screen.blit(self.background, (rel_x, rel_y))

        # additional bg
        if self.head.x_lab < - self.width/2 + self.bg_width or self.head.y_lab < - self.height/2 + self.bg_height:
            rel_x = W - (-self.head.x_lab) % self.bg_width
            rel_y = H - (-self.head.y_lab) % self.bg_height
            if rel_x < W:
                if self.head.x_lab < - self.width/2 + self.bg_width:
                    screen.blit(self.rock_bg, (-rel_x, H - rel_y))
                    screen.blit(self.rock_bg, (-rel_x, H - self.bg_height - rel_y))
            if rel_y < H:
                if self.head.y_lab < - self.height/2 + self.bg_height and rel_y > 0:
                    screen.blit(self.grass_bg, (self.bg_width - rel_x,
                                                H - self.bg_height - rel_y))
                    if rel_x < W:
                        screen.blit(self.grass_bg, (-rel_x, H - self.bg_height - rel_y))

    @staticmethod
    def generate(number_of_items, number_of_enemies):
        for j in range(number_of_items):
            new_item = Item(randint(-main_map.width/2 + main_map.bg_width - W/2,
                                    main_map.width/2 - main_map.bg_width + W/2),
                            randint(-main_map.height/2 + main_map.bg_height - H/2,
                                    main_map.height/2 - main_map.bg_height + H/2),
                            np.random.choice(["seed", "berry"], p=[0.9, 0.1]))
            list_of_items.add(new_item)
        for k in range(number_of_enemies):
            new_enemy = Enemy(randint(-main_map.width/2 + main_map.bg_width - W/2,
                                      main_map.width/2 - main_map.bg_width + W/2),
                              randint(-main_map.height/2 + main_map.bg_height - H/2,
                                      main_map.height/2 - main_map.bg_height + H/2),
                              worm)
            list_of_enemies.append(new_enemy)
            group_of_enemies.add(new_enemy)


class Worm:
    """Класс червя, управляемого игроком. Состоит из сегментов
    move() - двигает все сегменты
    new_segment() - Добавляет сегменты
    attack() - взаимодействие с врагом
    update() - отрисовка
    list_of_segments - список элементов класса segment, сегментов червя"""

    def __init__(self, group, list_s):
        self.list_of_segments = list_s
        self.head = list_of_segments[0]
        self.tail = list_of_segments[len(list_of_segments) - 1]
        self.group = group
        self.angle = 0
        self.health = 1
        self.boost_end = time.time()  # change
        self.boost_time = 5

    def move(self, x, y):
        """вижение на положение мыши"""
        if x != self.head.x:
            dir_angle = math.atan((y - self.head.y) / (x - self.head.x))
            if x - self.head.x < 0 and dir_angle < math.pi / 2:
                dir_angle += math.pi
        elif y > self.head.y:
            dir_angle = math.pi / 2
        else:
            dir_angle = -math.pi / 2
        self.angle = dir_angle

        self.head.vx = self.head.v * math.cos(self.angle)
        self.head.vy = self.head.v * math.sin(self.angle)
        self.set_speed()
        for segment in self.list_of_segments:
            segment.move()

    def set_speed(self):
        for count in range(1, len(self.list_of_segments)):
            previous = self.list_of_segments[count - 1]  # Предыдущий сегмент
            segment = self.list_of_segments[count]  # Текущий сегмент, скорость которого мы выставляем
            delta_y = previous.y - segment.y  # Разность у
            delta_x = previous.x - segment.x  # Разность х
            distance = math.sqrt(delta_x ** 2 + delta_y ** 2)  # Расстояние между сегментом и предыдущим
            future_distance = math.sqrt((previous.y + previous.vy - segment.y) ** 2 +
                                        (previous.x + previous.vx - segment.x) ** 2)
            segment.v = future_distance - 5  # constant distance
            segment.vx = segment.v * delta_x / distance  # Новая скорость
            segment.vy = segment.v * delta_y / distance  # Новая скорость

    def new_segment(self):
        """Добавляет сегмент за последним из текущих, координаты задаются рекуррентно"""
        previous_segment = self.list_of_segments[len(self.list_of_segments) - 1]
        before_previous_segment = self.list_of_segments[len(self.list_of_segments) - 2]
        x = 2 * previous_segment.x - before_previous_segment.x
        y = 2 * previous_segment.y - before_previous_segment.y
        self.list_of_segments.append(Segment(x, y))
        group_of_segments.add(self.list_of_segments[len(self.list_of_segments) - 1])

    def boost(self):
        self.boost_end = time.time() + self.boost_time

    def attack(self):
        pass

    def update(self):
        # boost
        if self.boost_end > time.time():
            self.head.v = 5
        else:
            self.head.v = 3

        # Moving worm
        group_of_segments.update()


class Segment(pygame.sprite.Sprite):
    """Класс сегмента, """

    def __init__(self, x, y):
        self.vx = 3
        self.vy = 0
        self.v = 3
        self.y = y  # screen coordinates
        self.x = x
        self.x_lab = x  # laboratory coordinates
        self.y_lab = y

        color = (181, 91, 91)
        alt_color = (125, 66, 66)

        super().__init__()
        self.image = pygame.Surface([20, 20], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        pygame.draw.circle(self.image, alt_color, (10, 10), 10, 1)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def move(self):
        if not - main_map.width/2 + main_map.bg_width/2 < self.x_lab + self.vx \
                < main_map.width/2 - main_map.bg_width/2 and self == worm.head:
            self.vx = 0
        if not - main_map.height/2 + main_map.bg_height - H/2 < self.y_lab + self.vy \
                < main_map.height/2 - main_map.bg_height + H/2 and self == worm.head:
            self.vy = 0

        # changing screen coordinates
        self.x += self.vx - list_of_segments[0].vx
        self.y += self.vy - list_of_segments[0].vy
        # changing laboratory coordinates
        self.x_lab += self.vx
        self.y_lab += self.vy

    def update(self):
        self.rect.center = [self.x, self.y]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        self.alive = True
        self.t = 0
        self.right = [0, 50, 100, 150, 200]
        self.left = [0, 50, 100, 150, 200]
        super().__init__()
        self.zone_x = x
        self.zone_y = y
        self.x_lab = x
        self.y_lab = y
        self.is_moving_right = True
        self.is_moving_left = False
        x = get_screen_cords(player.head, self.x_lab, self.y_lab)[0]
        y = get_screen_cords(player.head, self.x_lab, self.y_lab)[1]
        self.v = 2.5
        self.is_not_attacking = True
        self.full_image = pygame.image.load("beetle5.png").convert_alpha()
        self.full_image = pygame.transform.scale(self.full_image, (250, 200))
        self.rect = pygame.Rect(x, y, 50, 50)
        self.rect.topleft = [x, y]
        self.image = self.full_image.subsurface((100, 100), (50, 50))
        self.zone = pygame.image.load("new_cave.png").convert_alpha()
        self.zone = pygame.transform.scale(self.zone, (200, 60))
        self.type = choice(['Bug', 'Ant', 'Bird'])
        self.damage = 0.1

    def move(self):
        self.rect.topleft = get_screen_cords(worm.head, int(self.x_lab), int(self.y_lab))
        if self.alive:
            self.t += 1
            self.is_not_attacking = True
            if not self.attack(worm) and (self.x_lab - self.zone_x >= 0 or self.x_lab - self.zone_x <= 200) and \
                    self.y_lab == self.zone_y:
                self.be_home()
                self.is_not_attacking = True
            elif (self.x_lab - self.zone_x < 0 or self.x_lab - self.zone_x > 150 or self.y_lab != self.zone_y) \
                    and self.is_not_attacking:
                self.go_home()
        else:
            self.image = self.full_image.subsurface(50, 150, 50, 50)
            self.image = pygame.transform.rotate(self.image, 180)

    def go_home(self):
        self.is_moving_right = True
        self.is_moving_left = False
        dist = get_distance(self.x_lab, self.y_lab, self.zone_x + 75, self.zone_y)
        dx = self.x_lab - 75 - self.zone_x
        dy = self.y_lab - self.zone_y
        if dx >= 0:
            self.animate_left()
        else:
            self.animate_right()
        self.x_lab -= self.v * dx / dist
        self.y_lab -= self.v * dy / dist
        if abs(self.x_lab - 75 - self.zone_x) <= 1 and abs(self.y_lab - self.zone_y) <= 1:
            self.x_lab = self.zone_x + 75
            self.y_lab = self.zone_y

    def animate_right(self):
        num = int(self.t / 5) % 5
        x = self.right[num]
        self.image = self.full_image.subsurface((x, 100, 50, 50))

    def animate_left(self):
        num = int(self.t / 5) % 5
        x = self.left[num]
        self.image = self.full_image.subsurface((x, 150, 50, 50))

    def be_home(self):
        if self.x_lab <= self.zone_x + 150 and self.is_moving_right:
            self.x_lab += 1
            self.animate_right()
            if self.x_lab >= self.zone_x + 149:
                self.is_moving_right = False
                self.t = 0

        if self.x_lab >= self.zone_x and self.is_moving_left:
            self.x_lab -= 0.7
            self.animate_left()
            if self.x_lab <= self.zone_x + 1:
                self.is_moving_left = False
                self.t = 0

        if not (self.is_moving_left or self.is_moving_right):
            self.image = self.full_image.subsurface(0, 0, 50, 50)
            if self.t == 100:
                if self.x_lab < self.zone_x + 50:
                    self.is_moving_right = True
                else:
                    self.is_moving_left = True

    def animate(self):
        if get_screen_cords(worm.head, self.zone_x, self.zone_y)[0] < 2000 and \
                get_screen_cords(worm.head, self.zone_x, self.zone_y)[1] < 4050:
            screen.blit(self.zone, get_screen_cords(worm.head, self.zone_x, self.zone_y))

    def attack(self, player):
        dist = get_distance(player.tail.x_lab, player.tail.y_lab, self.x_lab + 25, self.y_lab + 25)
        if get_distance(player.head.x_lab, player.head.y_lab, self.x_lab + 25, self.y_lab + 25) <= 20:
            self.alive = False
        if get_distance(player.tail.x_lab, player.tail.y_lab, self.x_lab + 25, self.y_lab + 25) <= 3:
            player.health -= self.damage
        if dist <= 200:
            self.is_not_attacking = False
            dx = self.x_lab - player.tail.x_lab + 25
            dy = self.y_lab - player.tail.y_lab + 25
            if dx <= 0:
                self.animate_right()
            else:
                self.animate_left()
            self.x_lab -= self.v * dx / dist
            self.y_lab -= self.v * dy / dist
            if dist == 0:
                return True
        return False


class Item(pygame.sprite.Sprite):
    def __init__(self, x_lab, y_lab, item_type):
        super().__init__()
        self.x_lab = x_lab
        self.y_lab = y_lab
        self.x, self.y = get_screen_cords(list_of_segments[0], self.x_lab, self.y_lab)
        self.type = item_type

        self.head = list_of_segments[0]

        # Draw object
        self.image = pygame.image.load(self.type + ".png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    def eat_check(self):
        if self.x_lab - 20 < self.head.x_lab < self.x_lab + 20 and self.y_lab - 20 < self.head.y_lab < self.y_lab + 20:
            if self.type == "seed":
                worm.new_segment()
            elif self.type == "berry":
                worm.boost()
            return 1
        else:
            return 0

    # update the item
    def update(self):
        [self.x, self.y] = get_screen_cords(list_of_segments[0], self.x_lab, self.y_lab)
        self.rect.center = self.x, self.y


def draw_trace(points):
    """Червь оставляет след"""
    prev = points[len(points) - 1]
    dist = get_distance(prev[0], prev[1], worm.head.x_lab, worm.head.y_lab)
    if dist >= 2.9:
        points.append((worm.head.x_lab, worm.head.y_lab))
    for point in points:
        if get_distance(point[0], point[1], worm.head.x_lab, worm.head.y_lab) <= 1200:
            x = int(get_screen_cords(worm.head, point[0], point[1])[0])
            y = int(get_screen_cords(worm.head, point[0], point[1])[1])
            pygame.draw.circle(screen, BROWN, (x, y), 15)
            if points.index(point) >= 500:
                points.pop(0)


def get_screen_cords(head, x_lab, y_lab):
    x = x_lab - head.x_lab + head.x
    y = y_lab - head.y_lab + head.y
    return [x, y]


def get_distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    dist = math.sqrt(dy ** 2 + dx ** 2)
    return dist


# new list of segments
group_of_segments = pygame.sprite.Group()
list_of_segments = [Segment(W / 2, H / 2), Segment(W / 2 - 9, H / 2 - 9)]  # Первые 2 сегмента
group_of_segments.add(list_of_segments[0], list_of_segments[1])
for i in range(2, 20):
    segment_x = 2 * list_of_segments[i - 1].x - list_of_segments[i - 2].x
    segment_y = 2 * list_of_segments[i - 1].y - list_of_segments[i - 2].y
    list_of_segments.append(Segment(segment_x, segment_y))
    group_of_segments.add(list_of_segments[i])

# Map
main_map = Map(4*1024, 4*1024)

used_area = [(0, 0)]

worm = Worm(group_of_segments, list_of_segments)

# list of items and the
list_of_items = pygame.sprite.Group()

# list of enemies
test_enemy = Enemy(900, 500, worm)
list_of_enemies = [test_enemy]
group_of_enemies = pygame.sprite.Group()
group_of_enemies.add(test_enemy)

# Bars
health_bar = Bars("health", 60)
boost_bar = Bars("boost", 100)
group_of_bars = pygame.sprite.Group()
group_of_bars.add(health_bar, boost_bar)


bg_image = pygame.image.load("menu.jpg")
bg_image = pygame.transform.scale(bg_image, [W, H])
screen.blit(bg_image, (0, 0, W, H))
ng_active = pygame.image.load("ng_active.png")
ng = pygame.image.load("ng.png")


def show_menu(event):
    if event.type == pygame.MOUSEMOTION:
        if 450 <= event.pos[1] <= 600 and 410 <= event.pos[0] <= 610:
            screen.blit(ng_active, (410, 450))
        else:
            screen.blit(ng, (410, 450))
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
            450 <= event.pos[1] <= 600 and 410 <= event.pos[0] <= 610:
        main_map.generate(200, 50)
        return True


def game():
    game_over = False  # Закончена ли игра
    game_started = False

    while not game_over:
        clock.tick(FPS)
        pygame.display.flip()
        if game_started:
            # Draw all the objects, update
            main_map.update_bg()
            # Draw items
            draw_trace(used_area)
            for item in list_of_items:
                if item.eat_check():
                    list_of_items.remove(item)
            list_of_items.update()
            list_of_items.draw(screen)
            for enemy in list_of_enemies:
                enemy.move()
                enemy.animate()
            group_of_enemies.draw(screen)
            group_of_enemies.update()
            worm.update()
            group_of_segments.draw(screen)

            group_of_bars.update()
            group_of_bars.draw(screen)

            if pygame.mouse.get_pressed()[0]:
                worm.move(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if not game_started:
                game_started = show_menu(event)


game()
