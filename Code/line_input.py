from Code.settings import FPS, COLOR

from typing import Tuple
import pygame as pg

from Code.texts import TextMaxSize


class LineInput:
    def __init__(self, width: int, height: int, pos: Tuple[int, int], background_color: COLOR = '#808080',
                 font_color: COLOR = (255, 255, 255), font_type: str = None) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.pos = (0, 0)
        #
        self.flag = False
        self.tick = 0
        #
        self.font_color = font_color
        self.background_color = background_color
        #
        self.text = TextMaxSize('', width=None, height=height, font_color=font_color, font_type=font_type)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.render()

    def event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and self.flag:
            if event.key == pg.K_RETURN:
                self.flag = False
                self.tick = 0
            elif event.key == pg.K_BACKSPACE:
                self.text.set_text(self.text.text[:-1])
            else:
                self.text.set_text(self.text.text + event.unicode)
            self.render()
        try:
            if self.rect.collidepoint(*event.pos) and event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.flag = True
                self.tick = 0
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.flag = False
                self.tick = 0
        except AttributeError:
            pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(pg.Color(self.background_color))
        self.surface.blit(self.text.surface, self.pos)

    def draw(self, display: pg.Surface) -> None:
        self.tick = (self.tick + 1) % (2 * FPS + 1)
        display.blit(self.surface, self.rect)
        if self.flag and self.tick <= FPS:
            pg.draw.rect(
                display, pg.Color(self.font_color),
                (
                    self.rect.x + self.text.rect.x + self.text.rect.width, self.rect.y + self.text.rect.y,
                    int(round(self.text.rect.height / 10, 0)), self.rect.height
                )
            )
