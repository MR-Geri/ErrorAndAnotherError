from Code.dialogs import DialogInfo
from Code.settings import *

import pygame as pg
from typing import Tuple
from Code.sector_objects.entities import Entities
from Code.texts import max_size_list_text


class Base:
    def __init__(self, pos: Tuple[int, int], size_cell: int, board: list,
                 entities: Entities, dialog_info: DialogInfo) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.board = board
        self.entities = entities
        self.dialog_info = dialog_info
        #
        self.name = 'База MK0'
        self.energy = 1000
        self.hp = 1000
        self.distance_create = 1
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        self.surface.fill('#00FFC9')

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def info(self, panel) -> None:
        size = max_size_list_text(
            [self.name],
            panel.interface.width, panel.interface.height, PT_MONO)
        panel.line_0.set_text(self.name, size)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.render()

    def create_robot(self, robot: ALL_ROBOT) -> None:
        n_x, k_x = self.pos[0] - self.distance_create, self.pos[0] + self.distance_create + 1
        n_y, k_y = self.pos[1] - self.distance_create, self.pos[1] + self.distance_create + 1
        for i_y, y in enumerate(self.board):
            for i_x, x in enumerate(y):
                if k_y > i_y >= n_y and k_x > i_x >= n_x and \
                        type(x) not in SELL_BLOCKED and self.entities.entities_sector[i_y][i_x] is None:
                    self.entities.add(robot(pos=(i_x, i_y), size_cell=self.size_cell))
                    return
        self.dialog_info.show(['Вокруг базы нет места', 'для нового объекта'])
