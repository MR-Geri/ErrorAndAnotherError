from Code.settings import FPS, CLOCK

from typing import Tuple
import pygame as pg

from Code.texts import TextMaxSize


class LineInput:
    def __init__(self, width: int, height: int, pos: Tuple[int, int],
                 font_color: Tuple[int, int, int] = (255, 255, 255), font_type: str = None) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.pos = (0, 0)
        #
        self.text = TextMaxSize('', width=None, height=height, font_color=font_color, font_type=font_type)
        self.surface = pg.Surface((self.rect.width, self.rect.height))

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
            # self.draw()
        except AttributeError:
            pass

    def before_render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.blit(self.text.surface, self.pos)

    def draw(self, display: pg.Surface) -> None:
        display.blit(self.surface, self.rect)
