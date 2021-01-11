from Code.settings import *


class Processor:
    def __init__(self, entities: dict) -> None:
        self.tick_complete = 0
        self.tick = 0
        self.tick_update = int(round(FPS / CHANGE_TICK, 0))  # 2 раза за секунду
        self.day = True
        self.entities = entities

    def ticked(self) -> None:
        self.tick = (self.tick + 1) % (self.tick_update + 1)
        if self.tick == self.tick_update:
            self.tick_complete += 1
            self.update()
        if self.tick_complete % UPDATE_CHANGE_TIME:
            self.day = not self.day

    def update(self) -> None:
        for y in self.entities:
            for x in self.entities[y]:
                entity = self.entities[y][x]
                type_ = type(entity)
                if type_ in ROBOTS:
                    pass
                elif type_ in BASES:
                    if entity.generator is not None:
                        entity.generator.update(self.tick_complete)
