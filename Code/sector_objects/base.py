from Code.settings import *

import pygame as pg
from typing import Tuple


class Base:
    def __init__(self, pos: Tuple[int, int], size_cell: int) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        #
        self.energy = 1000
        self.hp = 1000
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        pos, size = 0.2 * self.size_cell, 0.6 * self.size_cell
        pg.draw.rect(self.surface, pg.Color('#00FFC9'), (pos, pos, size, size))

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.render()
