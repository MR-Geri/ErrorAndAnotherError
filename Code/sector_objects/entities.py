from Code.settings import *

from typing import Tuple
import pygame as pg


class Entities:
    def __init__(self, sector_size: Tuple[int, int]) -> None:
        self.sector_size = sector_size
        self.entities_sector = {y: {x: None for x in range(self.sector_size[0])} for y in range(self.sector_size[1])}

    def add(self, entity) -> None:
        x, y = entity.pos
        if self.entities_sector[y][x]:
            self.entities_sector[y][x].crash.play()
        self.entities_sector[y][x] = entity

    def render(self, surface: pg.Surface) -> None:
        for y in self.entities_sector:
            for x in self.entities_sector[y]:
                entity = self.entities_sector[y][x]
                if entity is not None:
                    surface.blit(entity.surface, entity.pos_draw)

    def scale(self, size_cell: int) -> None:
        for y in self.entities_sector:
            for x in self.entities_sector[y]:
                entity = self.entities_sector[y][x]
                if entity is not None:
                    entity.scale(size_cell)
