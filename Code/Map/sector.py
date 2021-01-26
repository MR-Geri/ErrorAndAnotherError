import importlib

from Code.settings import *

from Code.dialogs import DialogInfo, DialogFile, DialogState
from Code.info_panel import RightPanel, LeftPanel
from Code.sector_objects.bases import Base
from Code.sector_objects.entities import Entities
from Code.Map.biomes import GeneratorBiomes
from Code.sound import Sound


class Sector:
    def __init__(self, number_x: int, number_y: int, size_cell: int, sound: Sound, dialog_info: DialogInfo,
                 dialog_file: DialogFile, dialog_state: DialogState,
                 right_panel: RightPanel, left_panel: LeftPanel) -> None:
        self.number_x, self.number_y = number_x, number_y  # Длина и высота сектора в единицах
        self.size_cell = size_cell
        self.size_sector = (number_x * size_cell, number_y * size_cell)
        self.surface = pg.Surface(self.size_sector)
        self.board = None
        self.base = None
        self.sound = sound
        self.dialog_info = dialog_info
        self.dialog_file = dialog_file
        self.dialog_state = dialog_state
        self.right_panel = right_panel
        self.left_panel = left_panel
        # Инициализация
        self.gen_board()
        #
        self.entities = Entities((self.number_x, self.number_y), sound)
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

    def save(self) -> tuple:
        board = [
            [x.__class__.__name__ for x in y]
            for y in self.board
        ]
        entities = self.entities.save()
        return board, entities

    def load(self, board, entities, size_cell) -> None:
        self.board = [
            [STR_TO_OBJECT[board[y][x]](x, y, size_cell, self.right_panel) for x in range(self.number_x)]
            for y in range(self.number_y)
        ]
        for data in entities:
            entity = STR_TO_OBJECT[data['name']]
            if entity in BASES:
                entity = entity(
                    pos=data['pos'], size_cell=size_cell, board=board, entities=self.entities,
                    dialog_info=self.dialog_info, dialog_file=self.dialog_file, dialog_state=self.dialog_state,
                    right_panel=self.right_panel, left_panel=self.left_panel)
                self.base = entity
            elif entity in ROBOTS:
                entity = entity(
                    pos=data['pos'], size_cell=size_cell, dialog_info=self.dialog_info, dialog_file=self.dialog_file,
                    dialog_state=self.dialog_state, right_panel=self.right_panel, left_panel=self.left_panel)
            entity.load(data)
            self.entities.add(entity)
        self.render()

    def get_board(self) -> list:
        board = [[
            {'name': x.__class__.__name__, 'energy_passage': int(x.energy_passage)}
            for x in y] for y in self.board]
        return board

    def get_entities(self) -> list:
        entities = self.entities.entities_sector
        entities = [
            [entities[y][x].get_state() if entities[y][x] is not None else None for x in entities[y]]
            for y in entities
        ]
        return entities

    def update(self, tick_complete) -> None:
        board = self.get_board()
        robots = []
        for y in self.entities.entities_sector:
            for x in self.entities.entities_sector[y]:
                entity = self.entities.entities_sector[y][x]
                type_ = type(entity)
                if type_ in ROBOTS:
                    robots.append(entity)
                elif type_ in BASES:
                    entities = self.get_entities()
                    try:
                        code = entity.path_user_code.code()
                        if code:
                            module = entity.path_user_code.module()
                            if 'energy_transfer' in code:
                                importlib.reload(importlib.import_module(module))
                                entity.energy_transfer = importlib.import_module(module).energy_transfer
                        data = entity.energy_transfer_core(board=board, entities=entities)
                        if data:
                            for energy, who_pos in data:
                                self.energy_transfer(entity, energy, who_pos)
                    except FileNotFoundError:
                        pass
                    except IndexError:
                        pass
                    #
                    if entity.generator is not None and entity.permissions.can_generate:
                        entity.generator.update(tick_complete)
        if robots:
            for entity in robots:
                entities = self.get_entities()
                try:
                    code = entity.path_user_code.code()
                    if code:
                        module = entity.path_user_code.module()
                        if 'move' in code:
                            importlib.reload(importlib.import_module(module))
                            entity.move = importlib.import_module(module).move
                        if 'mine' in code:
                            importlib.reload(importlib.import_module(module))
                            entity.mine = importlib.import_module(module).mine
                    #
                    self.move(entity, entity.move_core(board=board, entities=entities))
                    self.mine(entity, entity.mine_core(board=board, entities=entities))
                    self.transfer(entity, *entity.transfer_core(board=board, entities=entities))
                    #
                except FileNotFoundError:
                    pass
                except IndexError:
                    pass
        self.render()

    def place_base(self, x: int, y: int) -> None:  # pos: Tuple[int, int]
        if type(self.board[y][x]) not in SELL_BLOCKED and not self.base and \
               0 <= y < SECTOR_Y_NUMBER and 0 <= x < SECTOR_X_NUMBER:
            self.base = Base(pos=(x, y), size_cell=self.size_cell, board=self.board, entities=self.entities,
                             dialog_info=self.dialog_info, dialog_file=self.dialog_file, dialog_state=self.dialog_state,
                             right_panel=self.right_panel, left_panel=self.left_panel)
            self.entities.add(self.base)
        else:
            if self.base:
                self.dialog_info.show(['База уже существует'])
            else:
                self.dialog_info.show(['Неподходящая поверхность для базы'])

    def energy_transfer(self, entity, energy: int, pos: Tuple[int, int]) -> None:
        if energy > 0 and pos:
            ent = self.entities.entities_sector[pos[1]][pos[0]]
            if ent.__class__.__name__ in entity.energy_possibility or ent is None:
                if abs(self.base.pos[0] - pos[0]) <= self.base.distance_charging and \
                        abs(self.base.pos[1] - pos[1]) <= self.base.distance_charging and self.base.energy >= energy \
                        and self.base.energy_max_charging >= energy:
                    if self.base.permissions.can_charging:
                        if self.entities.entities_sector[pos[1]][pos[0]] is not None:
                            self.entities.entities_sector[pos[1]][pos[0]].energy_receiving(energy)
                        self.base.energy_decrease(energy)
                        self.sound.add(self.base.sound_charge)

    def create_robot(self, robot: ALL_ROBOT) -> None:
        n_x, k_x = self.base.pos[0] - self.base.distance_create, self.base.pos[0] + self.base.distance_create + 1
        n_y, k_y = self.base.pos[1] - self.base.distance_create, self.base.pos[1] + self.base.distance_create + 1
        for i_y, y in enumerate(self.board):
            for i_x, x in enumerate(y):
                if k_y > i_y >= n_y and k_x > i_x >= n_x and \
                        type(x) not in SELL_BLOCKED and self.entities.entities_sector[i_y][i_x] is None:
                    robot_ = robot(pos=(i_x, i_y), size_cell=self.size_cell, dialog_file=self.dialog_file,
                                   dialog_info=self.dialog_info, dialog_state=self.dialog_state,
                                   right_panel=self.right_panel, left_panel=self.left_panel)
                    if self.base.energy >= robot_.energy_create:
                        self.base.energy -= robot_.energy_create
                        self.base.entities.add(robot_)
                        # Происходит обновление базы -> обновим панель
                        if self.right_panel.info_update == self.base.info:
                            self.base.info()
                    return
        self.dialog_info.show(['Вокруг базы нет места', 'для нового объекта'])

    def move(self, entity, pos: Tuple[int, int]) -> None:
        if pos and self.board[pos[1]][pos[0]].__class__.__name__ not in entity.sell_block:
            entities_sector = self.entities.entities_sector
            x, y = entity.pos
            if entity.distance_move >= abs(pos[1] - y) and entity.distance_move >= abs(pos[0] - x) \
                    and pos != (x, y) and entities_sector[y][x] is not None and 0 <= pos[0] < SECTOR_X_NUMBER and \
                    0 <= pos[1] < SECTOR_Y_NUMBER:
                if type(entities_sector[pos[1]][pos[0]]) in BASES:
                    self.sound.add(entities_sector[y][x].sound_crash)
                    entities_sector[y][x] = None
                elif entity.energy >= self.board[pos[1]][pos[0]].energy_passage:
                    entity.energy -= self.board[pos[1]][pos[0]].energy_passage
                    entities_sector[y][x] = None
                    if entities_sector[pos[1]][pos[0]] is not None:
                        self.sound.add(entities_sector[pos[1]][pos[0]].sound_crash)
                    entity.pos_update(pos)
                    entities_sector[pos[1]][pos[0]] = entity
                    self.sound.add(entities_sector[pos[1]][pos[0]].sound_move)

    def mine(self, entity, pos: Tuple[int, int]) -> None:
        if pos and self.board[pos[1]][pos[0]].__class__.__name__ in STR_ORES:
            x, y = entity.pos
            if abs(pos[1] - y) <= 1 and abs(pos[0] - x) <= 1 and \
                    0 <= pos[0] < SECTOR_X_NUMBER and 0 <= pos[1] < SECTOR_Y_NUMBER:
                cell = self.board[pos[1]][pos[0]]
                entity.inventory.update(resource=cell.ore, quantity=cell.ore_quantity)
                self.sound.add(entity.sound_mine)

    def transfer(self, entity, pos: Tuple[int, int], resource: str, condition: str, quantity: int) -> None:
        if resource in entity.inventory and (condition == 'сырьё' or condition == 'обработано'):
            print(self.board)

    def render(self) -> None:
        self.surface.fill(pg.Color(COLOR_BACKGROUND))
        for cells in self.board:
            for cell in cells:
                self.surface.blit(cell.image, cell.rect)
        self.entities.draw(self.surface)

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
