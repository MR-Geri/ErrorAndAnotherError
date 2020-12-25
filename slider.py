from typing import Tuple
import pygame as pg

from Code.settings import *


class Volume:
    def __init__(self, min_value: int, max_value: int, change: int) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.change = change
        self.value = (max_value - min_value) // 2

    def edit_volume(self, sign) -> None:
        self.value = min(self.max_value, max(self.min_value, self.value + sign * self.change))


class Slider:
    def __init__(self, pos: Tuple[int, int], width: int, height: int,
                 color_no_use: COLOR, color_use: COLOR, color_circle: COLOR, func) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.line = pg.Rect(pos[0], pos[1], width, self.rect.height // 4)
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
        self.surface = pg.Surface((self.rect.width, self.rect.height))  # , pg.SRCALPHA
        radius_main = self.rect.height // 2
        height = self.rect.height // 4
        mini_radius = height // 2
        width = self.rect.width - height
        pos = (mini_radius, (self.rect.height - height) // 2)
        pg.draw.circle(
            self.surface, self.color_no_use, (pos[0] + radius_main, pos[1] + mini_radius), mini_radius
        )
        pg.draw.circle(
            self.surface, self.color_no_use, (pos[0] + width - radius_main, pos[1] + mini_radius), mini_radius
        )
        pg.draw.rect(
            self.surface, self.color_no_use, (pos[0] + radius_main, pos[1], width - radius_main * 2, height)
        )
        w = self.rect.width - radius_main * 2 - mini_radius
        pg.draw.circle(
            self.surface,
            self.color_circle,
            (pos[0] + radius_main + (w * (self.func.value / self.func.max_value)),
             pos[1] + mini_radius),
            radius_main
        )


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
