from typing import Tuple

import pygame as pg


class Robot:
    def __init__(self, pos: Tuple[int, int], size_cell: int) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.pos_draw = (self.pos[0] * self.size_cell, self.pos[1] * self.size_cell)
        #
        self.energy = 0
        self.dmg = 0
        self.hp = 100
        #
        self.rect = pg.Rect(*self.pos, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        radius = int(self.size_cell / 2)
        pg.draw.circle(self.surface, pg.Color(0, 0, 0), (radius, radius), radius)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.pos_draw = (self.pos[0] * self.size_cell, self.pos[1] * self.size_cell)
        self.render()
