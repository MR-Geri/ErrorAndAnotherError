from typing import Tuple
import pygame as pg

from Code.settings import CLOCK, FPS
from Code.texts import TextMaxSizeCenter


class RunningLineMaxSizeCenter:
    def __init__(self, text: str, width: int, height: int, pos: Tuple[int, int], speed: int,
                 font_color: Tuple[int, int, int] = (255, 255, 255), font_type: str = None) -> None:
        self.text = text
        self.cl_text = TextMaxSizeCenter(
            f'  {self.text}  ', width=None, height=height, font_color=font_color, font_type=font_type
        )
        self.speed = speed
        self.font_color, self.font_type, self.height = font_color, font_type, height
        self.rect = pg.Rect(*pos, width, height)
        self.pos = (self.cl_text.rect.x, self.cl_text.rect.y)
        self.surface = pg.Surface((self.rect.width, self.rect.height))

    def render(self, display: pg.Surface) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.blit(self.cl_text.surface, self.pos)
        if self.pos[0] < -self.cl_text.rect.width + self.rect.width:
            self.surface.blit(self.cl_text.surface, (self.pos[0] + self.cl_text.rect.width, self.pos[1]))
        display.blit(self.surface, self.rect)

    def update(self, text) -> None:
        if text != self.text:
            self.text = text
            self.cl_text = TextMaxSizeCenter(
                f'  {self.text}', width=None, height=self.height, font_color=self.font_color, font_type=self.font_type
            )
            self.pos = (self.cl_text.rect.x, self.cl_text.rect.y)
        self.pos = (self.pos[0] - self.speed / max(FPS // 2, CLOCK.get_fps()), self.pos[1])
        if self.pos[0] < -self.cl_text.rect.width:
            self.pos = (0, self.pos[1])
