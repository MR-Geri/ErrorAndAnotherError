import pygame as pg
from Code.settings import CELL_COLOR
from Code.graphics import pg_random_color


class Cell(pg.sprite.Sprite):
    def __init__(self, number_x: int, number_y: int, size_cell: int) -> None:
        super().__init__()
        self.number_x, self.number_y = number_x, number_y
        self.x = number_x * size_cell
        self.y = number_y * size_cell
        self.size_cell = size_cell
        self.image = pg.Surface((size_cell, size_cell))
        self.rect = pg.Rect(self.x, self.y, self.size_cell, self.size_cell)
        #
        self.image.fill(pg_random_color())
        pg.draw.rect(self.image, pg.Color((255, 255, 255)), (10, 10, self.size_cell - 20, self.size_cell - 20))
