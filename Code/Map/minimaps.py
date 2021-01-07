from Code.settings import *

import pygame as pg
from typing import Tuple


class Minimap:
    def __init__(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.surface = pg.Surface((width, height))
        self.surface.fill((0, 0, 0))
        self.rect = pg.Rect(*pos, width, height)

    def render(self, surface: pg.Surface) -> None:
        self.surface = pg.transform.scale(surface, (self.rect.width, self.rect.height))
        # self.surface.fill((0, 0, 0))

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def update(self) -> None:
        pass
