from Code.settings import *
from Code.interface_utils import Txt
from Code.info_panel import RightPanel

import pygame as pg


class MK0:
    def __init__(self, pos: Tuple[int, int], size_cell: int, dialog_file, right_panel: RightPanel) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.right_panel = right_panel
        self.dialog_file = dialog_file
        #
        self.path_user_code = Txt('MK0')
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
        self.right_panel.info_update = self.info
        energy = f'Энергии > {self.energy}'
        hp = f'Прочности > {self.hp}'
        texts = [self.name, energy, hp]
        self.right_panel.update_text(texts)

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        radius = int(self.size_cell / 2)
        pg.draw.circle(self.surface, pg.Color(0, 0, 0), (radius, radius), radius)

    def func_file(self) -> None:
        self.dialog_file.show(self.path_user_code)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.render()
