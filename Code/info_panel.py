import pygame as pg
from Code.settings import *


class InfoPanels:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.panel_left_cord = (0, 0)
        self.panel_right_cord = (WIN_WIDTH - self.width, 0)
        self.panel_left, self.panel_right = None, None
        self.render()

    def render(self) -> None:
        self.panel_left = pg.Surface((self.width, self.height))
        self.panel_right = pg.Surface((self.width, self.height))
        #
        self.panel_left.fill(pg.Color((128, 128, 128)))
        self.panel_right.fill(pg.Color((128, 128, 128)))
