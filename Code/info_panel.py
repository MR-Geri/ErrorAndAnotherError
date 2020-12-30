from Code.settings import *

from typing import Tuple
import pygame as pg
import datetime

from Code.sound import Music
from Code.texts import TextMaxSizeCenter


class Panel:
    def __init__(self, width: int, height: int, pos: Tuple[int, int]) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.color_background = pg.Color((128, 128, 128))
        self.interface_indent = (0, self.rect.height // 50)
        self.interface_size = (self.rect.width, self.rect.height // 20)

    def get_absolute_pos(self, x: int, y: int) -> Tuple[int, int]:
        return self.rect.x + x, self.rect.y + y

    def render(self) -> None:
        pass

    def update(self) -> None:
        pass


class LeftPanel(Panel):
    def __init__(self, width: int, height: int, pos: Tuple[int, int], music: Music = None) -> None:
        super().__init__(width, height, pos)
        self.music = music
        self.running_line = RunningLineMaxSizeCenter(
            text='пример текста', width=self.interface_size[0], height=self.interface_size[1],
            pos=(self.interface_indent[0], self.interface_indent[1]), speed=30, font_type=PT_MONO
        )
        self.update()
        self.render()

    def update(self) -> None:
        self.running_line.update(self.music.get_text())

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(self.color_background)
        self.running_line.render(self.surface)


class RightPanel(Panel):
    def __init__(self, width: int, height: int, pos: Tuple[int, int]) -> None:
        super().__init__(width, height, pos)
        self.update()
        self.render()

    def update(self) -> None:
        text = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
        pos_ = (0, self.interface_indent[1])
        self.system_time = TextMaxSizeCenter(text=f'{text}', width=self.rect.width, pos=pos_,
                                             font_type=PT_MONO)
        pos_ = (0, pos_[1] + self.system_time.rect.height + self.interface_indent[1])

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(self.color_background)
        #
        self.surface.blit(self.system_time.surface, self.system_time.rect)
