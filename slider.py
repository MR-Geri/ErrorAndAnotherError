from typing import Tuple
import pygame as pg

from Code.settings import *


class Numbers:
    def __init__(self, min_value: int, max_value: int, change: int) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.change = change
        self.value = int((max_value - min_value) / 2)

    def edit(self, sign) -> None:
        self.value = min(self.max_value, max(self.min_value, self.value + sign * self.change))

    def set_value(self, value) -> None:
        self.value = min(self.max_value, max(self.min_value, value))


class Slider:
    def __init__(self, pos: Tuple[int, int], width: int, height: int,
                 color_no_use: COLOR, color_use: COLOR, color_circle: COLOR, func) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.circle = pg.Rect(*pos, self.rect.height, self.rect.height)
        self.func = func
        self.color_no_use = color_no_use
        self.color_use = color_use
        self.color_circle = color_circle
        #
        self.radius_main, self.rect_height = int(self.rect.height / 2), int(self.rect.height / 2.5)
        self.radius_mini = int(self.rect_height / 2)
        self.two_radius = self.radius_main + self.radius_mini
        self.rect_width = int(self.rect.width - 2 * self.radius_main - 2 * self.radius_mini)
        self.padding = int((self.rect.height - self.rect_height) / 2)
        self.pixel_size = self.rect_width + 2 * self.radius_mini
        self.pixel_change = self.pixel_size / self.func.max_value * self.func.change
        #
        self.flag_click = False
        self.render()

    def update(self, event: pg.event.Event) -> None:
        try:
            if self.rect.collidepoint(*event.pos):
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    self.flag_click = False
                if self.flag_click:
                    value = int((event.pos[0] - self.rect.x - self.radius_main) / self.pixel_change * self.func.change)
                    self.func.set_value(value)
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.flag_click:
                    self.flag_click = True
            else:
                self.flag_click = False
            self.render()
        except AttributeError:
            pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        pg.draw.circle(
            self.surface, self.color_use, (self.two_radius, self.padding + self.radius_mini), self.radius_mini
        )
        pg.draw.circle(
            self.surface, self.color_no_use,
            (self.rect.width - self.two_radius, self.padding + self.radius_mini), self.radius_mini
        )
        pg.draw.rect(
            self.surface, self.color_no_use, (self.two_radius, self.padding, self.rect_width, self.rect_height)
        )
        w_value = self.pixel_size * (self.func.value / self.func.max_value)
        pg.draw.rect(self.surface, self.color_use, (self.two_radius, self.padding, w_value, self.rect_height))
        self.circle.x = self.rect.x + w_value
        self.circle.y = self.rect.y + self.padding + self.radius_mini - self.radius_main
        pg.draw.circle(
            self.surface, self.color_circle,
            (self.radius_main + w_value, self.padding + self.radius_mini), self.radius_main
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
