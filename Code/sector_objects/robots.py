from Code.settings import *
from Code.utils import Path, PermissionsRobot
from Code.dialogs import DialogInfo, DialogFile
from Code.info_panel import RightPanel


class MK0:
    def __init__(self, pos: Tuple[int, int], size_cell: int,
                 dialog_info: DialogInfo, dialog_file: DialogFile, right_panel: RightPanel) -> None:
        self.pos = list(pos)  # Надо сохранять
        self.size_cell = size_cell
        self.right_panel = right_panel
        self.dialog_info = dialog_info
        self.dialog_file = dialog_file
        self.unique_name = str(randint(1000000, 9999999))  # Надо сохранять
        # Функции пользователя
        self.move = lambda *args, **kwargs: None
        # Состояния
        self.permissions = PermissionsRobot()  # Надо сохранять
        #
        self.path_user_code = Path('MK0')  # Надо сохранять
        self.name = 'Робот MK0'
        self.energy = 50  # Надо сохранять
        self.energy_max = 200  # Надо сохранять
        self.energy_create = 100
        self.dmg = 0  # Надо сохранять
        self.hp = 100  # Надо сохранять
        self.distance_move = 1  # Надо сохранять
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
        data = {
            'name': self.__class__.__name__, 'unique_name': self.unique_name,
            'pos': tuple(self.pos), 'x': self.pos[0], 'y': self.pos[1],
            'hp': self.hp,
            'energy': self.energy, 'energy_max': self.energy_max,
            'damage': self.dmg, 'dmg': self.dmg,
            'sell_block': self.sell_block, 'distance_move': self.distance_move
        }
        for k, v in data.items():
            data[k] = type(v)(v)
        data['permissions'] = self.permissions
        return data

    def pos_update(self, pos: Tuple[int, int]) -> None:
        # НЕ ВЛИЯЕТ пользователь
        self.pos = list(pos)
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        if self.right_panel.info_update == self.info:
            self.info()

    def energy_receiving(self, energy: int) -> None:
        # ВЛИЯЕТ пользователь
        if self.permissions.can_charging:
            self.energy = min(energy + self.energy, self.energy_max)
            if self.right_panel.info_update == self.info:
                self.info()

    def move_core(self, board, entities) -> Union[None, Tuple[int, int]]:
        # ВЛИЯЕТ пользователь
        if self.permissions.can_move:
            return self.move(self.get_state(), board, entities)
        return None

    def info(self) -> None:
        self.right_panel.info_update = self.info
        energy = f'Энергии > {self.energy}'
        energy_max = f'Макс. Энергии > {self.energy_max}'
        hp = f'Прочности > {self.hp}'
        move = f'Премещение > {self.distance_move}'
        texts = [self.name, 'Уникальное имя', self.unique_name, energy, energy_max, hp, move]
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

    def save(self) -> dict:  # Как мы будем "сохранять" класс
        state = {
            'pos': self.pos, 'unique_name': self.unique_name,
            'path_user_code': self.path_user_code.text, 'name': self.__class__.__name__, 'energy': self.energy,
            'energy_max': self.energy_max, 'dmg': self.dmg, 'hp': self.hp, 'distance_move': self.distance_move,
            'permissions': self.permissions.get_state()}  # 'energy_transfer': self.energy_transfer
        return state

    def load(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        self.pos = state['pos']
        self.unique_name = state['unique_name']
        self.path_user_code = Path(state['path_user_code'])
        self.energy = state['energy']
        self.energy_max = state['energy_max']
        self.hp = state['hp']
        self.dmg = state['dmg']
        self.distance_move = state['distance_move']
        #
        self.permissions = PermissionsRobot(state['permissions'])
