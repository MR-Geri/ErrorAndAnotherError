from Code.settings import *
from Code.sound import Sound


class Entities:
    def __init__(self, sector_size: Tuple[int, int], sound: Sound, bases) -> None:
        self.bases = bases
        self.sound = sound
        self.sector_size = sector_size
        self.entities_sector = {y: {x: None for x in range(self.sector_size[0])} for y in range(self.sector_size[1])}

    def add(self, entity) -> None:
        x, y = entity.pos
        if self.entities_sector[y][x]:
            self.sound.add(self.entities_sector[y][x].sound_crash)
        self.entities_sector[y][x] = entity

    def draw(self, surface: pg.Surface) -> None:
        for y in self.entities_sector:
            for x in self.entities_sector[y]:
                entity = self.entities_sector[y][x]
                if entity is not None:
                    entity.draw(surface)

    def scale(self, size_cell: int) -> None:
        for y in self.entities_sector:
            for x in self.entities_sector[y]:
                entity = self.entities_sector[y][x]
                if entity is not None:
                    entity.scale(size_cell)

    def move(self, entity, pos: Tuple[int, int]) -> None:
        x, y = entity.pos
        if entity.distance_move >= abs(pos[1] - y) and entity.distance_move >= abs(pos[0] - x) and pos != (x, y) and  \
                self.entities_sector[y][x] is not None and 0 <= pos[0] < SECTOR_X_NUMBER and \
                0 <= pos[1] < SECTOR_Y_NUMBER:
            if type(self.entities_sector[pos[1]][pos[0]]) in self.bases:
                self.sound.add(self.entities_sector[y][x].sound_crash)
                self.entities_sector[y][x] = None
            else:
                self.entities_sector[y][x] = None
                if self.entities_sector[pos[1]][pos[0]] is None:
                    entity.update_pos(pos)
                    self.entities_sector[pos[1]][pos[0]] = entity
                    self.sound.add(self.entities_sector[pos[1]][pos[0]].sound_move)
                else:
                    self.sound.add(self.entities_sector[pos[1]][pos[0]].sound_crash)
