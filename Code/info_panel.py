from typing import Tuple

import pygame as pg
import datetime

from Code.settings import *
from Code.utils import Text


class Panel:
    def __init__(self, width: int, height: int, pos: Tuple[int, int]) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.color_background = pg.Color((128, 128, 128))
        self.update()
        self.render()

    def get_absolute_pos(self, x: int, y: int) -> Tuple[int, int]:
        return self.rect.x + x, self.rect.y + y


class LeftPanel(Panel):
    def __init__(self, width: int, height: int, pos: Tuple[int, int]) -> None:
        super().__init__(width, height, pos)

    def update(self) -> None:
        pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(self.color_background)


class RightPanel(Panel):
    def __init__(self, width: int, height: int, pos: Tuple[int, int]) -> None:
        super().__init__(width, height, pos)

    def update(self) -> None:
        text = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
        self.system_time = Text(text=f'{text}', pos=(15, 10), font_size=30)

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(self.color_background)
        #
        self.surface.blit(self.system_time.surface, self.system_time.rect)
