import pygame as pg
from random import choice

pg.init()
screen = pg.display.set_mode((700, 900))

FPS = 30


class Screen:
    def init(self):
        pass

    def move(self):
        pass

    def update(self):
        pass


class Worm:
    def __init__(self):
        pass

    def move(self):
        pass

    def resize(self):
        pass

    def attack(self):
        pass

    def update(self):
        pass


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
    pass
