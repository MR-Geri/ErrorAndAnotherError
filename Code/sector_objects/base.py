from Code.interface_utils import Txt
from Code.settings import *
from Code.dialogs import DialogInfo
from Code.info_panel import RightPanel
from Code.sector_objects.generates_electrical import RadioisotopeGenerator

import pygame as pg
from Code.sector_objects.entities import Entities


class Base:
    def __init__(self, pos: Tuple[int, int], size_cell: int, board: list, entities: Entities,
                 dialog_info: DialogInfo, dialog_file, right_panel: RightPanel) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.board = board
        self.entities = entities
        self.dialog_info = dialog_info
        self.dialog_file = dialog_file
        self.right_panel = right_panel
        #
        self.path_user_code = Txt('Пусто')
        self.name = 'База MK0'
        self.energy = 1000
        self.energy_max = 1500
        self.hp = 1000
        self.distance_create = 1
        # Установленные предметы
        self.generator = RadioisotopeGenerator(self.generation_energy)
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        self.surface.fill('#00FFC9')
        if self.generator:
            self.generator.draw(self.surface, self.rect)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def info(self) -> None:
        print(self.path_user_code.text)
        self.right_panel.info_update = self.info
        energy = f'Энергии > {self.energy}'
        hp = f'Прочность > {self.hp}'
        distance = f'Дистанция базы > {self.distance_create}'
        texts = [self.name, energy, hp, distance, 'Установленные модули']
        if self.generator:
            texts.append(f'<{self.generator.name}>')
        self.right_panel.update_text(texts)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.render()

    def generation_energy(self, energy: int):
        self.energy += energy if self.energy + energy <= self.energy_max else 0
        if self.right_panel.info_update == self.info:
            self.info()

    def func_file(self) -> None:
        self.dialog_file.show(self.path_user_code)

    def create_robot(self, robot: ALL_ROBOT) -> None:
        n_x, k_x = self.pos[0] - self.distance_create, self.pos[0] + self.distance_create + 1
        n_y, k_y = self.pos[1] - self.distance_create, self.pos[1] + self.distance_create + 1
        for i_y, y in enumerate(self.board):
            for i_x, x in enumerate(y):
                if k_y > i_y >= n_y and k_x > i_x >= n_x and \
                        type(x) not in SELL_BLOCKED and self.entities.entities_sector[i_y][i_x] is None:
                    robot_ = robot(pos=(i_x, i_y), size_cell=self.size_cell, dialog_file=self.dialog_file,
                                   right_panel=self.right_panel)
                    if self.energy >= robot_.energy_create:
                        self.energy -= robot_.energy_create
                        self.entities.add(robot_)
                        # Происходит обновление базы -> обновим панель
                        if self.right_panel.info_update == self.info:
                            self.info()
                    return
        self.dialog_info.show(['Вокруг базы нет места', 'для нового объекта'])
