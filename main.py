import pygame
import math
from random import randint

W = 1024
H = 720
screen = pygame.display.set_mode((W, H))

FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
pygame.init()
clock = pygame.time.Clock()


class Map:
    def __init__(self):
        self.head = list_of_segments[0]  # Worm head
        self.background = pygame.image.load("bg.png")

    def update_bg(self):
        # Moving background
        rel_x = W - self.head.x_lab % self.background.get_rect().width
        rel_y = H - self.head.y_lab % self.background.get_rect().height
        screen.blit(self.background, (rel_x - self.background.get_rect().width,
                                      rel_y - self.background.get_rect().height))
        if rel_x < W:
            screen.blit(self.background, (rel_x, rel_y - self.background.get_rect().height))
        if rel_y < H:
            screen.blit(self.background, (rel_x - self.background.get_rect().width, rel_y))
        if rel_x < W and rel_y < H:
            screen.blit(self.background, (rel_x, rel_y))


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
        self.group = group
        self.angle = 0

    def move(self, x, y):
        """вижение на положение мыши"""
        if x != self.head.x:
            dir_angle = math.atan((y-self.head.y)/(x-self.head.x))
            if x - self.head.x < 0 and dir_angle < math.pi/2:
                dir_angle += math.pi
        elif y > self.head.y:
            dir_angle = math.pi/2
        else:
            dir_angle = -math.pi/2
        self.angle = dir_angle

        self.head.vx = self.head.v*math.cos(self.angle)
        self.head.vy = self.head.v*math.sin(self.angle)
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
            segment.v = future_distance - 7  # FIX change to constant distance
            segment.vx = segment.v * delta_x / distance  # Новая скорость
            segment.vy = segment.v * delta_y / distance  # Новая скорость

    def new_segment(self):
        """Добавляет сегмент за последним из текущих, координаты задаются рекуррентно"""
        previous_segment = self.list_of_segments[len(self.list_of_segments) - 1]
        before_previous_segment = self.list_of_segments[len(self.list_of_segments) - 2]
        x = 2*previous_segment.x - before_previous_segment.x
        y = 2*previous_segment.y - before_previous_segment.y
        self.list_of_segments += Segment("rand", x, y)

    def attack(self):
        pass

    def update(self):
        # Moving worm
        group_of_segments.update()


class Segment(pygame.sprite.Sprite):
    """Класс сегмента, """

    def __init__(self, color, x, y):
        self.vx = 3
        self.vy = 0
        self.v = 3
        self.y = y  # screen coordinates
        self.x = x
        self.x_lab = x  # laboratory coordinates
        self.y_lab = y

        """if color == "rand":
            color1 = randint(0, 255)
            color2 = randint(0, 255)
            color3 = randint(0, 255)
            color = (color1, color2, color3)"""
        color = (181, 91, 91)
        alt_color = (125, 66, 66)

        super().__init__()
        self.image = pygame.Surface([20, 20], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        pygame.draw.circle(self.image, alt_color, (10, 10), 10, width=1)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def move(self):
        # changing screen coordinates
        self.x += self.vx - list_of_segments[0].vx
        self.y += self.vy - list_of_segments[0].vy
        # changing laboratory coordinates
        self.x_lab += self.vx
        self.y_lab += self.vy

    def update(self):
        self.rect.center = [self.x, self.y]


"""class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.zone_x = x
        self.zone_y = y
        self.x_lab = x
        self.y_lab = y
        self.x = -50
        self.y = -50
        self.v = 3
        self.image = pygame.image.load("beetle5.png")
        self.left = False
        self.right = False
        self.stay = True
        self.image = pygame.transform.scale(self.image, (25*5, 25*4)).convert_alpha()
        self.rect = pygame.Rect((25, 0), (25, 25))
        self.rect.center = [x, y]
        self.zone = pygame.image.load("RockBG.png")
        self.zone = pygame.transform.scale(self.zone, (100, 30))
        self.type = choice(['Bug', 'Ant', 'Bird'])

    def move(self):
        pass

    def animate(self, head):
        if  < 900:
            screen.blit(self.zone, [self.zone_x - get_head_cords(head)[0], self.zone_y - get_head_cords(head)[1]])

    def attack(self, player):
        pass

    def update(self):
        pass"""


class Item(pygame.sprite.Sprite):
    def __init__(self, x_lab, y_lab, item_type):
        super().__init__()
        self.x_lab = x_lab
        self.y_lab = y_lab
        self.x, self.y = get_screen_cords(list_of_segments[0], self.x_lab, self.y_lab)
        self.type = item_type

        # Berry
        self.image = pygame.image.load(self.type + ".png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    # update the item, will change later
    def update(self):
        [self.x, self.y] = get_screen_cords(list_of_segments[0], self.x_lab, self.y_lab)
        self.rect.center = self.x, self.y


def draw_trace(points, player):
    """Червь оставляет след"""
    prev = points[len(points) - 2]
    dist = math.sqrt((prev[0]-player.head.x)**2 + (prev[1]-player.head.y)**2)
    if dist >= 10:
        points.append((player.head.x, player.head.y))


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
list_of_segments = [Segment(RED, W / 2, H / 2), Segment('rand', W / 2 - 9, H / 2 - 9)]  # Первые 2 сегмента
group_of_segments.add(list_of_segments[0], list_of_segments[1])
for i in range(2, 20):
    segment_x = 2*list_of_segments[i - 1].x - list_of_segments[i - 2].x
    segment_y = 2*list_of_segments[i - 1].y - list_of_segments[i - 2].y
    list_of_segments.append(Segment('rand', segment_x, segment_y))
    group_of_segments.add(list_of_segments[i])
# test_segment = Segment(100, 100)
# list_of_segments.add(test_segment)

# Map
map = Map()

used_area = []

# list of items and the
test_item = Item(500, 500, "berry")
test_item_2 = Item(400, 400, "seed")
list_of_items = pygame.sprite.Group()
list_of_items.add(test_item, test_item_2)

'''# list of enemies
test_enemy = Enemy(500, 300)
list_of_enemies = pygame.sprite.Group()
list_of_enemies.add(test_enemy)
group_of_enemies = pygame.sprite.Group()
group_of_enemies.add(Enemy(100, 100))'''

worm = Worm(group_of_segments, list_of_segments)


def game():
    game_over = False  # Закончена ли игра

    while not game_over:
        clock.tick(FPS)

        # Draw all the objects, update
        pygame.display.flip()
        map.update_bg()
        # Draw items
        '''for enemy in list_of_enemies:
            enemy.move()
            enemy.animate(worm.head)
        group_of_enemies.draw(screen)'''
        list_of_items.update()
        list_of_items.draw(screen)
        worm.update()
        group_of_segments.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if pygame.mouse.get_pressed()[0]:
            worm.move(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


game()
