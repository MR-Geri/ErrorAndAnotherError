from Code.settings import *
from Code.utils import Path, PermissionsBase
from Code.dialogs import DialogInfo, DialogFile
from Code.info_panel import RightPanel, LeftPanel
from Code.sector_objects.entities import Entities


class Base:
    def __init__(self, pos: Tuple[int, int], size_cell: int, board: list, entities: Entities,
                 dialog_info: DialogInfo, dialog_file: DialogFile, right_panel: RightPanel,
                 left_panel: LeftPanel) -> None:
        self.pos = list(pos)  # Надо сохранять
        self.size_cell = size_cell
        self.board = board
        self.entities = entities
        self.dialog_info = dialog_info
        self.dialog_file = dialog_file
        self.right_panel = right_panel
        self.left_panel = left_panel
        # Функции пользователя
        self.energy_transfer = lambda *args, **kwargs: None
        # Состояния
        self.permissions = PermissionsBase()  # Надо сохранять
        # Характеристики
        self.path_user_code = Path('')  # Надо сохранять
        self.name = 'База MK0'
        self.energy = 1000  # Надо сохранять
        self.energy_max = 4000  # Надо сохранять
        self.hp = 1000  # Надо сохранять
        self.distance_create = 1  # Надо сохранять
        self.distance_charging = 1  # Надо сохранять
        self.energy_max_charging = 5  # Надо сохранять
        self.energy_possibility = ['MK0']
        #
        self.sound_charge = PATH_CHARGE + 'MK0.wav'
        # Установленные предметы
        self.generator = RadioisotopeGenerator(self.energy_increase)  # Надо сохранять
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def get_state(self) -> dict:
        data = {
            'pos': tuple(self.pos), 'x': self.pos[0], 'y': self.pos[1], 'hp': self.hp, 'energy': self.energy,
            'energy_max': self.energy_max, 'distance_create': self.distance_create,
            'distance_charging': self.distance_charging, 'energy_possibility': self.energy_possibility,
            'energy_max_charging': self.energy_max_charging
        }
        for k, v in data.items():
            data[k] = type(v)(v)
        data['permissions'] = self.permissions
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
        energy_max = f'Макс. Энергии > {self.energy_max}'
        distance_charging = f'Дист. Зарядки > {self.distance_charging}'
        energy_max_charging = f'Макс. Передача > {self.energy_max_charging}'
        distance_create = f'Дист. Создания > {self.distance_create}'
        hp = f'Прочность > {self.hp}'
        texts = [self.name, energy, energy_max, distance_charging, energy_max_charging, distance_create, hp,
                 'Установленные модули']
        if self.generator:
            texts.append(f'<{self.generator.name}>')
        self.right_panel.update_text(texts)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.render()

    def energy_increase(self, energy: int) -> None:
        # НЕ ВЛИЯЕТ пользователь
        self.energy += energy if self.energy + energy <= self.energy_max else 0
        if self.right_panel.info_update == self.info:
            self.info()

    def energy_decrease(self, energy: int) -> None:
        # НЕ ВЛИЯЕТ пользователь
        self.energy -= energy
        if self.right_panel.info_update == self.info:
            self.info()

    def energy_transfer_core(self, board, entities) -> Union[None, list]:
        # НЕ ВЛИЯЕТ пользователь
        return self.energy_transfer(self.get_state(), board, entities)

    def func_file(self) -> None:
        self.dialog_file.show(self.path_user_code)  # Установка файла

    def func_del_file(self) -> None:
        self.path_user_code.set_text('')
        self.left_panel.button_del_file.func = None

    def save(self) -> dict:  # Как мы будем "сохранять" класс
        state = {
            'pos': self.pos,
            'path_user_code': self.path_user_code.text, 'name': self.__class__.__name__, 'energy': self.energy,
            'energy_max': self.energy_max, 'hp': self.hp, 'distance_create': self.distance_create,
            'distance_charging': self.distance_charging, 'energy_max_charging': self.energy_max_charging,
            'generator': self.generator.__class__.__name__, 'generator_resource': self.generator.resource,
            'permissions': self.permissions.get_state()}
        # 'energy_transfer': self.energy_transfer
        return state

    def load(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        self.pos = state['pos']
        self.path_user_code = Path(state['path_user_code'])
        self.energy = state['energy']
        self.energy_max = state['energy_max']
        self.hp = state['hp']
        self.distance_create = state['distance_create']
        self.distance_charging = state['distance_charging']
        self.energy_max_charging = state['energy_max_charging']
        self.generator = STR_TO_OBJECT[state['generator']](self.energy_increase, state['generator_resource'])
        self.permissions = PermissionsBase(state['permissions'])
