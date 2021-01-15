from Code.settings import *
from Code.utils import Path
from Code.info_panel import RightPanel


class MK0:
    def __init__(self, pos: Tuple[int, int], size_cell: int, dialog_file, right_panel: RightPanel) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.right_panel = right_panel
        self.dialog_file = dialog_file
        # Функции пользователя
        self.move = lambda *args, **kwargs: None
        #
        self.path_user_code = Path('MK0')
        self.name = 'Робот MK0'
        self.energy = 50
        self.energy_max = 150
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
        data = {
            'name': self.__class__.__name__, 'pos': self.pos, 'x': self.pos[0], 'y': self.pos[1], 'hp': self.hp,
            'energy': self.energy, 'energy_max': self.energy_max, 'damage': self.dmg, 'dmg': self.dmg,
            'sell_block': self.sell_block, 'distance_move': self.distance_move
        }
        for k, v in data.items():
            data[k] = type(v)(v)
        return data

    def pos_update(self, pos: Tuple[int, int]) -> None:
        self.pos = list(pos)
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        if self.right_panel.info_update == self.info:
            self.info()

    def energy_receiving(self, energy: int) -> None:
        self.energy = min(energy + self.energy, self.energy_max)
        if self.right_panel.info_update == self.info:
            self.info()

    def move_core(self, board, entities) -> Union[None, Tuple[int, int]]:
        return self.move(self.get_state(), board, entities)

    def info(self) -> None:
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
