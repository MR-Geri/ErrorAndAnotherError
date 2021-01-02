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

    def event(self, event: pg.event.Event) -> None:
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

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def update_text(self) -> None:
        pass


class ButtonTwoStates(Button):
    def __init__(self, pos: Tuple[int, int], width: int, height: int, color_disabled: COLOR, color_active: COLOR,
                 text: ALL_TEXT, texts: Tuple[str, str], get_state, func):
        self.texts = texts
        self.text = text
        self.get_state = get_state
        super().__init__(pos=pos, width=width, height=height, color_disabled=color_disabled, color_active=color_active,
                         text=self.text, func=func)

    def event(self, event: pg.event.Event) -> None:
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

    def update_text(self) -> None:
        self.text.set_text(self.texts[self.get_state()])
        self.render()


class Buttons:
    def __init__(self) -> None:
        self.buttons = []

    def add(self, button: Button) -> None:
        self.buttons.append(button)

    def event(self, event: pg.event.Event) -> None:
        for button in self.buttons:
            button.event(event)

    def draw(self, surface: pg.Surface) -> None:
        for button in self.buttons:
            button.draw(surface)

    def update_text(self) -> None:
        for button in self.buttons:
            button.update_text()
