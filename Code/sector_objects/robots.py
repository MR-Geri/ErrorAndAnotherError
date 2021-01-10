from Code.info_panel import RightPanel
from Code.settings import *

from typing import Tuple
import pygame as pg

from Code.texts import max_size_list_text


class MK0:
    def __init__(self, pos: Tuple[int, int], size_cell: int, panel: RightPanel) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.panel = panel
        #
        self.name = 'Робот MK0'
        self.energy = 0
        self.energy_create = 100
        self.dmg = 0
        self.hp = 100
        #
        self.crash = PATH_CRASHES + 'robot.wav'
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def info(self) -> None:
        self.panel.info_update = self.info
        energy = f' Энергии > {self.energy} '
        hp = f' Прочности > {self.hp} '
        texts = [self.name, energy, hp]
        self.panel.update_text(texts)

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        radius = int(self.size_cell / 2)
        pg.draw.circle(self.surface, pg.Color(0, 0, 0), (radius, radius), radius)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.render()
