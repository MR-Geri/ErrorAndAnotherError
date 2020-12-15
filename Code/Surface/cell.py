import pygame as pg
from math import ceil

from Code.settings import CELL_COLOR
from Code.graphics import pg_random_color


class Cell(pg.sprite.Sprite):
    def __init__(self, number_x: int, number_y: int, size_cell: int) -> None:
        super().__init__()
        self.number_x, self.number_y = number_x, number_y
        self.x = number_x * size_cell
        self.y = number_y * size_cell
        self.size_cell = size_cell
        self.color = pg_random_color()
        #
        self.render(size_cell)

    def render(self, size_cell):
        self.size_cell = size_cell
        self.x = self.number_x * size_cell
        self.y = self.number_y * size_cell
        self.image = pg.Surface((self.size_cell, self.size_cell))
        self.rect = pg.Rect(self.x, self.y, self.size_cell, self.size_cell)
        #
        self.image.fill(self.color)
        pg.draw.rect(
            self.image,
            pg.Color((255, 255, 255)),
            (
                int(0.25 * self.size_cell),
                int(0.25 * self.size_cell),
                ceil(0.5 * self.size_cell),
                ceil(0.5 * self.size_cell)
            )
        )
