import pygame as pg
from Code.settings import *
from Code.sector_objects.entities import Entities
from Code.utils import Path
from Code.info_panel import RightPanel


class MK0:
    def __init__(self, pos: Tuple[int, int], size_cell: int, dialog_file, right_panel: RightPanel, board: list,
                 entities: Entities) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.right_panel = right_panel
        self.dialog_file = dialog_file
        self.board = board
        self.entities = entities
        #
        self.move = lambda *args, **kwargs: None
        #
        self.path_user_code = Path('MK0')
        self.name = 'Робот MK0'
        self.energy = 0
        self.energy_create = 100
        self.dmg = 0
        self.hp = 100
        self.distance_move = 1
        self.sell_block = ['Mountain']
        #
        self.sound_crash = PATH_CRASHES + 'MK0.wav'
        self.sound_move = PATH_MOVES + 'MK0.wav'
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def get_state(self) -> dict:
        return {
            'pos': self.pos, 'x': self.pos[0], 'y': self.pos[1], 'hp': self.hp, 'energy': self.energy,
            'damage': self.dmg, 'dmg': self.dmg
        }

    def update_pos(self, pos: Tuple[int, int]) -> None:
        self.pos = list(pos)
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)

    def move_my(self, board, entities) -> Union[None, Tuple[int, int]]:
        return self.move(self.get_state()['pos'], board, entities)

    def info(self) -> None:
        print(self.path_user_code.text)
        self.right_panel.info_update = self.info
        energy = f'Энергии > {self.energy}'
        hp = f'Прочности > {self.hp}'
        move = f'Премещение > {self.distance_move}'
        texts = [self.name, energy, hp, move]
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
