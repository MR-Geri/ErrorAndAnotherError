from Code.settings import *
from Code.dialogs import DialogInfo, DialogFile, DialogState
from Code.info_panel import RightPanel, LeftPanel


class Enemy:
    def __init__(self, pos: Tuple[int, int], size_cell: int, dialog_info: DialogInfo, dialog_file: DialogFile,
                 dialog_state: DialogState, right_panel: RightPanel, left_panel: LeftPanel) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.right_panel = right_panel
        self.left_panel = left_panel
        self.dialog_info = dialog_info
        self.dialog_file = dialog_file
        self.dialog_state = dialog_state
        # Заменяются классом противника
        self.name = 'Противник'
        self.dmg = 0
        self.hp = 0
        self.hp_max = 0
        self.distance_move = 0
        self.sell_block = ['Mountain'] + STR_ORES
        # Заменяются классом противника
        self.sound_crash = PATH_CRASHES + 'MK0.ogg'
        self.sound_move = PATH_MOVES + 'MK0.ogg'
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def get_state(self) -> dict:
        data = {
            'name': self.__class__.__name__, 'pos': tuple(self.pos), 'x': self.pos[0], 'y': self.pos[1],
            'hp': self.hp, 'damage': self.dmg, 'dmg': self.dmg, 'sell_block': self.sell_block,
            'distance_move': self.distance_move
        }
        for k, v in data.items():
            data[k] = type(v)(v)
        return data

    def pos_update(self, pos: Tuple[int, int]) -> None:
        self.pos = list(pos)
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        if self.right_panel.info_update == self.info:
            self.info()

    def info(self) -> None:
        self.right_panel.info_update = self.info
        hp = f'Прочность > {self.hp}'
        texts = [self.name, hp]
        self.right_panel.update_text(texts)

    def save(self) -> dict:
        state = {
            'pos': self.pos, 'name': self.__class__.__name__, 'dmg': self.dmg, 'hp': self.hp, 'hp_max': self.hp_max,
            'distance_move': self.distance_move
        }
        return state

    def load(self, state: dict):
        self.pos = state['pos']
        self.hp = state['hp']
        self.hp_max = state['hp_max']
        self.dmg = state['dmg']
        self.distance_move = state['distance_move']

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        pg.draw.polygon(self.surface, pg.Color(255, 255, 255),
                        [
                            (int(self.size_cell / 2), 0),
                            (0, self.size_cell),
                            (self.size_cell, self.size_cell)
                        ])

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.render()


class Warrior(Enemy):
    def __init__(self, pos: Tuple[int, int], size_cell: int, dialog_info: DialogInfo, dialog_file: DialogFile,
                 dialog_state: DialogState, right_panel: RightPanel, left_panel: LeftPanel) -> None:
        super().__init__(pos, size_cell, dialog_info, dialog_file, dialog_state, right_panel, left_panel)
        self.name = 'Воин'
        self.dmg = 0
        self.hp = 100
        self.hp_max = 100
        self.distance_move = 1
        self.sell_block = ['Mountain'] + STR_ORES
