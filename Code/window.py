import pygame as pg
from typing import Tuple
from Code.settings import *


class Window:
    def __init__(self, size_display: Tuple[int, int], caption: str) -> None:
        self.caption = caption
        self.is_run = False
        #
        self.display = pg.display.set_mode(size_display)
        pg.display.set_caption(self.caption)
        self.bd = pg.Surface(size_display)
        self.bd.fill(pg.Color(BACKGROUND_COLOR))


class MenuWindow(Window):
    def __init__(self, size_display: Tuple[int, int], caption: str):
        super().__init__(size_display, caption)

    def run(self):
        self.is_run = True
        while self.is_run:
            for en in pg.event.get():
                if en.type == pg.QUIT:
                    pg.quit()
                    quit()
            self.display.blit(self.bd, (0, 0))
            pg.display.update()
