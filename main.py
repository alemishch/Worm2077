import pygame
import math
from random import choice, randint

W = 1024
H = 720
screen = pygame.display.set_mode((W, H))
background = pygame.image.load("background.jpg")

FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
pygame.init()
clock = pygame.time.Clock()


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
        """вижение на WASD"""
        self.angle = math.atan(self.head.vy/self.head.vx)
        dir_angle = math.atan((y-self.head.y)/(x-self.head.x))

        if dir_angle - self.angle > 0:
            self.angle += 0.2
        elif dir_angle - self.angle < 0:
            self.angle -= 0.2

        if x - self.head.x < 0:
            self.angle += math.pi

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
        pass


class Segment(pygame.sprite.Sprite):
    """Класс сегмента, """

    def __init__(self, color, x, y):
        self.vx = 5
        self.vy = 0
        self.v = 5
        self.y = y
        self.x = x

        if color == "rand":
            color1 = randint(0, 255)
            color2 = randint(0, 255)
            color3 = randint(0, 255)
            color = (color1, color2, color3)

        super().__init__()
        self.image = pygame.Surface([20, 20], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 10, )
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def update(self):
        # Moving background
        rel_x = self.x % background.get_rect().width
        rel_y = self.y % background.get_rect().height
        screen.blit(background, (rel_x - background.get_rect().width, rel_y - background.get_rect().height))
        if rel_x < W:
            screen.blit(background, (rel_x, rel_y - background.get_rect().height))
        if rel_y < H:
            screen.blit(background, (rel_x - background.get_rect().width, rel_y))
        if rel_x < W and rel_y < H:
            screen.blit(background, (rel_x, rel_y))

        self.rect.center = [self.x, self.y]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.v = 3
        self.image = pygame.image.load("bug.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.type = choice(['Bug', 'Ant', 'Bird'])

    def move(self):
        pass

    def attack(self, player):
        pass

    def update(self):
        pass


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("berry.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.type = choice(["Seed", "Corpse", "Berry"])

    # update the item, will change later
    def update(self):
        self.rect.center = pygame.mouse.get_pos()


def draw_trace(points, player):
    """Червь оставляет след"""
    prev = points[len(points) - 2]
    dist = math.sqrt((prev[0]-player.head.x)**2 + (prev[1]-player.head.y)**2)
    if dist >= 10:
        points.append((player.head.x, player.head.y))


# new list of segments
group_of_segments = pygame.sprite.Group()
list_of_segments = [Segment(RED, W / 2, H / 2), Segment('rand', W / 2 - 9, H / 2 - 9)]  # Первые 2 сегмента
group_of_segments.add(list_of_segments[0], list_of_segments[1])
for i in range(2, 11):
    segment_x = 2*list_of_segments[i - 1].x - list_of_segments[i - 2].x
    segment_y = 2*list_of_segments[i - 1].y - list_of_segments[i - 2].y
    list_of_segments.append(Segment('rand', segment_x, segment_y))
    group_of_segments.add(list_of_segments[i])
# test_segment = Segment(100, 100)
# list_of_segments.add(test_segment)

used_area = []

# list of items and the
test_item = Item(500, 500)
list_of_items = pygame.sprite.Group()
list_of_items.add(test_item)

# list of enemies
test_enemy = Enemy(500, 300)
list_of_enemies = pygame.sprite.Group()
list_of_enemies.add(test_enemy)

worm = Worm(group_of_segments, list_of_segments)


def game():
    game_over = False  # Закончена ли игра

    while not game_over:
        clock.tick(FPS)

        # Draw all the objects, update
        pygame.display.flip()

        # group_of_enemies.draw(screen)
        group_of_segments.update()
        group_of_segments.draw(screen)
        # list_of_items.draw(screen)
        # list_of_items.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if pygame.mouse.get_pressed()[0]:
            worm.move(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


game()
