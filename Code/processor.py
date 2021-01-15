import importlib

from Code.settings import *


class Processor:
    def __init__(self, sector) -> None:
        self.tick_complete = 0
        self.tick = 0
        self.tick_update = int(round(FPS / CHANGE_TICK, 0))  # 2 раза за секунду
        self.day = True
        self.sector = sector
        self.entities = sector.entities
        self.board = sector.board
        #
        self.robots = []

    def ticked(self) -> None:
        self.tick = (self.tick + 1) % (self.tick_update + 1)
        if self.tick == self.tick_update:
            self.tick_complete += 1
            self.update()
        if self.tick_complete % UPDATE_CHANGE_TIME:
            self.day = not self.day

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

    def update(self) -> None:
        board = self.get_board()
        self.robots = []
        for y in self.entities.entities_sector:
            for x in self.entities.entities_sector[y]:
                entity = self.entities.entities_sector[y][x]
                type_ = type(entity)
                if type_ in ROBOTS:
                    self.robots.append(entity)
                elif type_ in BASES:
                    if entity.generator is not None:
                        entity.generator.update(self.tick_complete)
        if self.robots:
            for entity in self.robots:
                entities = self.get_entities()
                try:
                    code = entity.path_user_code.code()
                    if code:
                        module = entity.path_user_code.module()
                        if 'move' in code:
                            importlib.reload(importlib.import_module(module))
                            entity.move = importlib.import_module(module).move
                    who_pos = entity.move_core(board=board, entities=entities)
                    if who_pos and board[who_pos[1]][who_pos[0]]['name'] not in entity.sell_block:
                        self.sector.move(entity, who_pos)
                except FileNotFoundError:
                    pass
                except IndexError:
                    pass
                except Exception as e:
                    print(f'Processor update Exception -> {e}')
            self.sector.render()
