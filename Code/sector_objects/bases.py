from Code.settings import *
from Code.utils import Path
from Code.dialogs import DialogInfo
from Code.info_panel import RightPanel
from Code.sector_objects.generates_electrical import RadioisotopeGenerator
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
        # Функции пользователя
        self.energy_transfer = lambda *args, **kwargs: None
        #
        self.path_user_code = Path('Base')
        self.name = 'База MK0'
        self.energy = 1000
        self.energy_max = 1500
        self.hp = 1000
        self.distance_create = 1
        self.distance_charging = 1
        self.energy_max_charging = 5
        self.energy_possibility = ['MK0']
        #
        self.sound_charge = PATH_CHARGE + 'MK0.wav'
        # Установленные предметы
        self.generator = RadioisotopeGenerator(self.energy_generation)
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def get_state(self) -> dict:
        data = {
            'pos': self.pos, 'x': self.pos[0], 'y': self.pos[1], 'hp': self.hp, 'energy': self.energy,
            'energy_max': self.energy_max, 'distance_create': self.distance_create,
            'distance_charging': self.distance_charging, 'energy_possibility': self.energy_possibility,
            'energy_max_charging': self.energy_max_charging
        }
        for k, v in data.items():
            data[k] = type(v)(v)
        return data

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        self.surface.fill('#00FFC9')
        if self.generator:
            self.generator.draw(self.surface, self.rect)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def info(self) -> None:
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

    def energy_generation(self, energy: int) -> None:
        self.energy += energy if self.energy + energy <= self.energy_max else 0
        if self.right_panel.info_update == self.info:
            self.info()

    def energy_return(self, energy: int) -> None:
        self.energy -= energy
        if self.right_panel.info_update == self.info:
            self.info()

    def energy_transfer_core(self, board, entities) -> Union[None, Tuple[int, Tuple[int, int]]]:
        return self.energy_transfer(self.get_state(), board, entities)

    def func_file(self) -> None:
        self.dialog_file.show(self.path_user_code)  # Установка файла
