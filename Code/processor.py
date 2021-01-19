import importlib

from Code.settings import *


class Processor:
    def __init__(self, sector, tick_complete=0, tick=0) -> None:
        self.tick_complete = tick_complete
        self.tick = tick
        self.tick_update = int(round(FPS / CHANGE_TICK, 0))  # 2 раза за секунду
        self.day = True
        self.sector = sector
        self.entities = sector.entities
        self.board = sector.board

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
                                if energy > 0:
                                    ent = self.entities.entities_sector[who_pos[1]][who_pos[0]]
                                    if who_pos and ent.__class__.__name__ in entity.energy_possibility or ent is None:
                                        self.sector.energy_transfer(energy, who_pos)
                    except FileNotFoundError:
                        pass
                    except IndexError:
                        pass
                    except Exception as e:
                        print(f'Processor base Exception -> {e}')
                    #
                    if entity.generator is not None and entity.permissions.can_generate:
                        entity.generator.update(self.tick_complete)
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
                    who_pos = entity.move_core(board=board, entities=entities)
                    if who_pos and board[who_pos[1]][who_pos[0]]['name'] not in entity.sell_block:
                        self.sector.move(entity, who_pos)
                except FileNotFoundError:
                    pass
                except IndexError:
                    pass
                except Exception as e:
                    print(f'Processor robots Exception -> {e}')
            self.sector.render()
