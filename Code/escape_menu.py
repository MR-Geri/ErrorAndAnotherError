from Code.settings import *
from typing import Tuple

import pygame as pg


class EscMenu:
    def __init__(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.fill(pg.Color(COLOR_BACKGROUND))
        self.if_active = False
