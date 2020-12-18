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

    def update(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.flag = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.flag:
            self.flag = True
            self.func()
        try:
            if self.rect.collidepoint(*event.pos):
                self.color = self.color_active
                self.render()
            else:
                self.color = self.color_disabled
                self.render()
        except AttributeError:
            pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(pg.Color(self.color))
        self.surface.blit(self.text.surface, self.text.rect)


class Buttons:
    def __init__(self) -> None:
        self.buttons = []

    def add(self, button: Button) -> None:
        self.buttons.append(button)

    def update(self, event: pg.event.Event) -> None:
        for button in self.buttons:
            button.update(event)

    def render(self, display: pg.Surface) -> None:
        for button in self.buttons:
            display.blit(button.surface, button.rect)
