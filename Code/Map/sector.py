from Code.settings import *

from Code.dialogs import DialogInfo
from Code.info_panel import RightPanel
from Code.sector_objects.base import Base
from Code.sector_objects.entities import Entities
from Code.Map.biomes import GeneratorBiomes
from Code.sound import Sound


class Sector:
    def __init__(self, number_x: int, number_y: int, size_cell: int, sound: Sound, dialog_info: DialogInfo,
                 dialog_file, right_panel: RightPanel) -> None:
        self.number_x, self.number_y = number_x, number_y  # Длина и высота сектора в единицах
        self.size_cell = size_cell
        self.size_sector = (number_x * size_cell, number_y * size_cell)
        self.surface = pg.Surface(self.size_sector)
        self.board = None
        self.base = None
        self.sound = sound
        self.dialog_info = dialog_info
        self.dialog_file = dialog_file
        self.right_panel = right_panel
        # Данные
        self.is_base: bool = False
        # Инициализация
        self.gen_board()
        #
        self.entities = Entities((self.number_x, self.number_y), sound=sound)
        #
        self.render()

    def gen_board(self) -> None:
        """
        Генерация сектора.
        """
        biomes = GeneratorBiomes(
            number_x=self.number_x,
            number_y=self.number_y,
            size_cell=self.size_cell,
            right_panel=self.right_panel
        )
        self.board = [
            [biomes.get_cell(x, y) for x in range(self.number_x)]
            for y in range(self.number_y)
        ]

    def place_base(self, pos: Tuple[int, int]) -> None:
        if type(self.board[pos[1]][pos[0]]) not in SELL_BLOCKED and not self.is_base:
            self.is_base = True
            self.base = Base(pos=pos, size_cell=self.size_cell, board=self.board, entities=self.entities,
                             dialog_info=self.dialog_info, dialog_file=self.dialog_file, right_panel=self.right_panel)
            self.entities.add(self.base)
        else:
            if self.is_base:
                self.dialog_info.show(['База уже существует'])
            else:
                self.dialog_info.show(['Неподходящая поверхность для базы'])

    def render(self) -> None:
        self.surface.fill(pg.Color(COLOR_BACKGROUND))
        for cells in self.board:
            for cell in cells:
                self.surface.blit(cell.image, cell.rect)
        self.entities.draw(self.surface)

    def move(self, entity, pos: Tuple[int, int]) -> None:
        entities_sector = self.entities.entities_sector
        x, y = entity.pos
        if entity.distance_move >= abs(pos[1] - y) and entity.distance_move >= abs(pos[0] - x) and pos != (x, y) and \
                entities_sector[y][x] is not None and 0 <= pos[0] < SECTOR_X_NUMBER and \
                0 <= pos[1] < SECTOR_Y_NUMBER:
            if type(entities_sector[pos[1]][pos[0]]) in BASES:
                self.sound.add(entities_sector[y][x].sound_crash)
                entities_sector[y][x] = None
            else:
                entities_sector[y][x] = None
                if entities_sector[pos[1]][pos[0]] is None:
                    entity.update_pos(pos)
                    entities_sector[pos[1]][pos[0]] = entity
                    self.sound.add(entities_sector[pos[1]][pos[0]].sound_move)
                else:
                    self.sound.add(entities_sector[pos[1]][pos[0]].sound_crash)

    def scale(self, size_cell) -> None:
        self.size_cell = size_cell
        self.size_sector = (self.number_x * size_cell, self.number_y * size_cell)
        self.surface = pg.Surface(self.size_sector)
        for cells in self.board:
            for cell in cells:
                cell.scale(size_cell)
        self.entities.scale(size_cell=size_cell)
        self.render()

    def draw(self, surface: pg.Surface, pos: Tuple[int, int]) -> None:
        surface.blit(self.surface, pos)
