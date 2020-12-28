from typing import Tuple, List
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
        self.flag_click = False
        self.render()

    def update(self, event: pg.event.Event) -> None:
        try:
            if self.rect.collidepoint(*event.pos):
                self.color = self.color_active
                if event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.flag_click:
                    self.flag_click = False
                    self.func()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.flag_click:
                    self.flag_click = True
            else:
                self.color = self.color_disabled
            self.render()
        except AttributeError:
            pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(pg.Color(self.color))
        self.surface.blit(self.text.surface, self.text.rect)


class ButtonTwoStates(Button):
    def __init__(self, pos: Tuple[int, int], width: int, height: int, color_disabled: COLOR, color_active: COLOR,
                 list_text: List[ALL_TEXT, ...],  func):
        self.list_text = list_text
        super().__init__(pos=pos, width=width, height=height, color_disabled=color_disabled, color_active=color_active,
                         text=self.list_text[0], func=func)

    def update(self, event: pg.event.Event) -> None:
        try:
            if self.rect.collidepoint(*event.pos):
                self.color = self.color_active
                if event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.flag_click:
                    self.flag_click = False
                    self.func()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.flag_click:
                    self.flag_click = True
            else:
                self.color = self.color_disabled
            self.render()
        except AttributeError:
            pass


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
