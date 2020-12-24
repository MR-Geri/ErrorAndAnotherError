from typing import Tuple
import pygame as pg

from Code.settings import *


def volume():
    pass


class Slider:
    def __init__(self, pos: Tuple[int, int], width: int, height: int,
                 color_no_use: COLOR, color_use: COLOR, color_circle: COLOR, func) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.func = func
        self.color_no_use = color_no_use
        self.color_use = color_use
        self.color_circle = color_circle
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
            self.render()
        except AttributeError:
            pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        radius_main = self.rect.height // 2
        height = self.rect.height // 2
        mini_radius = height // 2
        width = self.rect.width - height
        pos = (mini_radius, (self.rect.height - height) // 2)
        pg.draw.circle(self.surface, self.color_no_use, (pos[0], pos[1] + mini_radius), mini_radius)
        pg.draw.circle(self.surface, self.color_no_use, (width + mini_radius, pos[1] + mini_radius), mini_radius)
        pg.draw.rect(self.surface, self.color_no_use, (pos[0], pos[1], width, height))


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
