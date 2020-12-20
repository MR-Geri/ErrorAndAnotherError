from typing import Tuple
import pygame as pg
import datetime

from Code.settings import *
from Code.texts import TextMaxSizeCenter


class Panel:
    def __init__(self, width: int, height: int, pos: Tuple[int, int]) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.color_background = pg.Color((128, 128, 128))
        self.indent_height = self.rect.height // 100
        self.update()
        self.render()

    def get_absolute_pos(self, x: int, y: int) -> Tuple[int, int]:
        return self.rect.x + x, self.rect.y + y

    def render(self) -> None:
        pass

    def update(self) -> None:
        pass


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
        pos_ = (0, self.indent_height)
        self.system_time = TextMaxSizeCenter(text=f'{text}', width=self.rect.width, pos=pos_,
                                             font_type=PT_MONO)
        pos_ = (0, pos_[1] + self.system_time.rect.height + self.indent_height)

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(self.color_background)
        #
        self.surface.blit(self.system_time.surface, self.system_time.rect)
