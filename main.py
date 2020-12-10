import pygame
import math
from random import choice

FPS = 30
W = 700
H = 500

pygame.init()
clock = pygame.time.Clock
pic = pygame.display.set_mode((W, H))


class Screen:
    """Главный экран. Отвечает за отрисовку и генерирование мира"""

    def __init__(self):
        self.list_of_items = []

    def move(self):
        pass

    def update(self):
        pass


class Worm:
    """Класс червя, управляемого игроком. Состоит из сегментов
    move() - двигает все сегменты
    new_segment() - Добавляет сегменты
    attack() - взаимодействие с врагом
    update() - отрисовка
    list_of_segments - список элементов класса segment, сегментов червя"""

    def __init__(self):
        self.list_of_segments = [Segment(W / 2, H / 2)]  # Первый сегмент - голова
        for i in range(1, 11):
            segment_x = self.list_of_segments[i - 1].x - self.list_of_segments[i - 2].x
            segment_y = self.list_of_segments[i - 1].y - self.list_of_segments[i - 2].y
            self.list_of_segments += Segment(segment_x, segment_y)

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

    def set_speed(self):
        for i in range(0, len(self.list_of_segments)):
            previous = self.list_of_segments[i-1]  # Предыдущий сегмент
            segment = self.list_of_segments[i]  # Текущий сегмент, скорость которого мы выставляем
            delta_y = previous.y - segment.y  # Разность у
            delta_x = previous.x - segment.x  # Разность х
            distance = math.sqrt(delta_x**2 + delta_y**2)  # Расстояние между сегментом и предыдущим
            segment.vx = segment.v * delta_x / distance  # Новая скорость
            segment.vy = segment.v * delta_y / distance  # Новая скорость

    def new_segment(self):
        """Добавляет сегмент за последним из текущих, координаты задаются рекуррентно"""
        previous_segment = self.list_of_segments[len(self.list_of_segments) - 1]
        before_previous_segment = self.list_of_segments[len(self.list_of_segments) - 2]
        x = previous_segment.x - before_previous_segment.x
        y = previous_segment.y - before_previous_segment.y
        self.list_of_segments += Segment(x, y)

    def attack(self):
        pass

    def update(self):
        pass


class Segment:
    """Класс сегмента, """

    def __init__(self, x, y):
        self.vx = 5
        self.vy = 5
        self.v = 10
        self.y = y
        self.x = x

    def move_segment_up(self):
        self.y -= self.vy

    def move_segment_down(self):
        self.y += self.vy

    def move_segment_left(self):
        self.x -= self.vx

    def move_segment_right(self):
        self.x += self.vx


class Enemy:
    def __init__(self):
        self.type = choice(['Bug', 'Ant', 'Bird'])

    def move(self):
        pass

    def attack(self, player):
        pass

    def update(self):
        pass


class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = choice(["Seed", "Corpse", "Berry"])


screen = Screen()
worm = Worm()


def game():
    game_over = False  # Закончена ли игра
    while not game_over:
        # clock.tick(FPS)
        for event in pygame.event.get():
            if event == pygame.QUIT:
                game_over = True
            if event == pygame.KEYDOWN:
                worm.move(event)
            screen.update()


game()
