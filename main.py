import pygame
import math
from random import choice

W = 1024
H = 720
screen = pygame.display.set_mode((W, H))
background = pygame.image.load("background.jpg")

FPS = 60
BLACK = (0, 0, 0)
pygame.init()
clock = pygame.time.Clock()


class Worm:
    """Класс червя, управляемого игроком. Состоит из сегментов
    move() - двигает все сегменты
    new_segment() - Добавляет сегменты
    attack() - взаимодействие с врагом
    update() - отрисовка
    FIX list_of_segments - список элементов класса segment, сегментов червя"""

    def __init__(self, group, list_s):
        self.list_of_segments = list_s
        self.group = group

    def move(self, event):
        """вижение на WASD"""
        self.set_speed()
        if event.key == pygame.K_w:
            for segment in self.list_of_segments:
                segment.move_segment_up()
        elif event.key == pygame.K_s:
            for segment in self.list_of_segments:
                segment.move_segment_down()
        elif event.key == pygame.K_d:
            for segment in self.list_of_segments:
                segment.move_segment_right()
        elif event.type == pygame.K_a:
            for segment in self.list_of_segments:
                segment.move_segment_left()
        # print(self.list_of_segments[0].x, self.list_of_segments[0].y)

    def set_speed(self):
        for i in range(0, len(self.list_of_segments)):
            previous = self.list_of_segments[i - 1]  # Предыдущий сегмент
            segment = self.list_of_segments[i]  # Текущий сегмент, скорость которого мы выставляем
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
        self.list_of_segments += Segment(x, y)

    def attack(self):
        pass

    def update(self):
        pass


class Segment(pygame.sprite.Sprite):
    """Класс сегмента, """

    def __init__(self, x, y):
        self.vx = 5
        self.vy = 5
        self.v = 10
        self.y = y
        self.x = x

        super().__init__()
        self.image = pygame.Surface([20, 20])
        pygame.draw.circle(self.image, (255, 255, 255), (10, 10), 10, )
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def move_segment_up(self):
        self.y -= self.vy
        self.rect.center = [self.x, self.y]

    def move_segment_down(self):
        self.y += self.vy
        self.rect.center = [self.x, self.y]

    def move_segment_left(self):
        self.x -= self.vx
        self.rect.center = [self.x, self.y]

    def move_segment_right(self):
        self.x += self.vx
        self.rect.center = [self.x, self.y]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
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


# new list of segments
group_of_segments = pygame.sprite.Group()
list_of_segments = [Segment(W / 2, H / 2), Segment(W / 2 - 5, H / 2 - 5)]  # Первый сегмент - голова
group_of_segments.add(list_of_segments[0], list_of_segments[1])
for i in range(2, 11):
    segment_x = 2*list_of_segments[i - 1].x - list_of_segments[i - 2].x
    segment_y = 2*list_of_segments[i - 1].y - list_of_segments[i - 2].y
    list_of_segments.append(Segment(segment_x, segment_y))
    group_of_segments.add(list_of_segments[i])
# test_segment = Segment(100, 100)
# list_of_segments.add(test_segment)

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

    # testing moving background
    x = 0
    while not game_over:
        clock.tick(FPS)

        # Draw all the objects, update
        pygame.display.flip()

        # Moving background
        rel_x = x % background.get_rect().width
        screen.blit(background, (rel_x - background.get_rect().width, 0))
        if rel_x < W:
            screen.blit(background, (rel_x, 0))
        x -= 2

        # group_of_enemies.draw(screen)
        group_of_segments.update()
        group_of_segments.draw(screen)
        # list_of_items.draw(screen)
        # list_of_items.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                worm.move(event)


game()
