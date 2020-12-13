import pygame as pg
from Code.settings import *


class InfoPanel:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.panel_left = pg.Surface((self.width, self.height))
        self.panel_left_cord = (0, 0)
        self.panel_right = pg.Surface((self.width, self.height))
        self.panel_right_cord = (WIN_WIDTH - self.width, 0)

    def render(self) -> None:
        pass
