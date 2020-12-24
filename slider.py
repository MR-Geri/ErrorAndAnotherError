from typing import Tuple
import pygame as pg

from Code.settings import *


def volume():
    pass


class Slider:
    def __init__(self, pos: Tuple[int, int], width: int, height: int,
                 color_no_use: COLOR, color_use: COLOR,  func) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.func = func
        self.color_no_use = color_no_use
        self.color_use = color_use
        self.flag = False
        self.render()

    def update(self, event: pg.event.Event) -> None:
        # Если мы зажали кружок -> линейно изменяем
        # Если мы два раза тыкнули по линии -> Перемещаем кружок туда (меняем значение)
        try:
            if self.rect.collidepoint(*event.pos):
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    self.flag = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.flag:
                    self.flag = True
                    self.func()
            else:
                self.color = self.color_disabled
            self.render()
        except AttributeError:
            pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        # Рисовать надо


class Sliders:
    def __init__(self) -> None:
        self.sliders = []

    def add(self, button: Slider) -> None:
        self.sliders.append(button)

    def update(self, event: pg.event.Event) -> None:
        for slider in self.sliders:
            slider.update(event)

    def render(self, display: pg.Surface) -> None:
        for slider in self.sliders:
            display.blit(slider.surface, slider.rect)
