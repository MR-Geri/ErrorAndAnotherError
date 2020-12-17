from typing import Tuple
import pygame as pg

from Code.settings import *


class Button:
    def __init__(self, pos: Tuple[int, int], width: int, height: int, color_disabled: COLOR, color_active: COLOR,
                 text: ALL_TEXT,  func) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.func = func
        self.text = text
        self.color_disabled = color_disabled
        self.color_active = color_active
        self.color = self.color_disabled
        self.flag = False
        self.render()

    def update(self, event) -> None:
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.flag = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.flag:
            self.flag = True
            self.func()
        try:
            if self.rect.collidepoint(*event.pos):
                print(1)
        except Exception as e:
            print(e)

    def focus(self) -> None:
        self.color = self.color_active

    def no_focus(self) -> None:
        self.color = self.color_disabled

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(pg.Color(self.color))
        self.surface.blit(self.text.surface, self.text.rect)


class Buttons:
    def __init__(self) -> None:
        pass
