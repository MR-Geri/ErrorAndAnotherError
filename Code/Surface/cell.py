import pygame as pg
from Code.settings import *


class Cell(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, size_cell: int) -> None:
        super().__init__()
        self.size_cell = size_cell
        #
        self.image = pg.Surface((size_cell, size_cell))
        self.image.fill(pg.Color(CELL_COLOR))
        self.image.set_colorkey(pg.Color(CELL_COLOR))
        self.rect = pg.Rect(x, y, size_cell, size_cell)
