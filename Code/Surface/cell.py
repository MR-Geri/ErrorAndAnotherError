import pygame as pg
from Code.settings import *
from random import randint


def render(surface, x, y, size_cell):
    print(x, y)
    pg.draw.rect(surface, pg.Color((255, 255, 255)), (x + 10, y + 10, size_cell - 20, size_cell - 20))


class Cell(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, size_cell: int) -> None:
        super().__init__()
        x *= size_cell
        y *= size_cell
        self.size_cell = size_cell
        #
        self.image = pg.Surface((size_cell, size_cell))
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.image.fill(pg.Color(color))
        render(self.image, x, y, size_cell)
        self.rect = pg.Rect(x, y, size_cell, size_cell)
