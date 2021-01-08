from Code.buttons import Button
from Code.interface_utils import Interface
from Code.settings import *

import pygame as pg
from typing import Tuple

from Code.texts import max_size_list_text


class DialogInfo:
    def __init__(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.fill(pg.Color('#25B2B9'))
        width_ = self.rect.width - self.rect.width // 50
        self.button = Button(
            pos=(
                pos[0] + self.rect.width // 100,
                pos[1] + self.rect.height - self.rect.height // 5 - self.rect.height // 100
            ),
            width=width_, height=self.rect.height // 5,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40), func=self.hide,
            text=TextMaxSizeCenter(text='Понятно', width=width_, height=self.rect.height // 5, font_type=PT_MONO)
        )
        self.if_active: bool = False

    def hide(self) -> None:
        self.if_active = False
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.fill(pg.Color('#25B2B9'))

    def event(self, event: pg.event.Event) -> None:
        self.button.event(event)

    def show(self, texts: list) -> None:
        self.if_active = True
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.fill(pg.Color('#25B2B9'))
        interface = Interface(pos=(0, self.rect.height // 100), max_width=self.rect.width,
                              max_height=self.rect.height - self.rect.height // 10,
                              indent=(0, self.rect.height // 100), size=(self.rect.width, self.rect.height // 5))
        size = max_size_list_text(texts, interface.width, interface.height, font_type=PT_MONO)
        for text in texts:
            _text = TextCenter(text, width=interface.width, height=interface.height, pos=interface.pos,
                               font_type=PT_MONO, font_size=size)
            self.surface.blit(_text.surface, _text.rect)
            interface.move(0)

    def draw(self, surface: pg.Surface) -> None:
        if self.if_active:
            surface.blit(self.surface, self.rect)
            self.button.draw(surface)
