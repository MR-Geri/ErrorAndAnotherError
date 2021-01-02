from Code.settings import FPS, COLOR

from typing import Tuple
import pygame as pg

from Code.texts import TextMaxSize


class LineInput:
    def __init__(self, width: int, height: int, pos: Tuple[int, int], background_color: COLOR = '#808080',
                 font_color: COLOR = (255, 255, 255), font_type: str = None) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.pos = [0, 0]
        self.pos_cursor = [0, 0]
        #
        self.flag = False
        self.tick = 0
        #
        self.font_color = font_color
        self.background_color = background_color
        #
        self.text = TextMaxSize('', width=None, height=height, font_color=font_color, font_type=font_type)
        self.char = TextMaxSize('F', width=None, height=height, font_color=font_color, font_type=font_type).rect.width
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.render()

    def event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and self.flag:
            if event.key == pg.K_RETURN:
                self.flag = False
                self.tick = 0
            elif event.key == pg.K_BACKSPACE:
                self.text.set_text(self.text.text[:-1])
            elif event.key == pg.K_LEFT:
                self.pos_cursor[0] = max(self.pos_cursor[0] - 1, 0)
            elif event.key == pg.K_RIGHT:
                self.pos_cursor[0] = min(self.pos_cursor[0] + 1, int(self.rect.width / self.char))
            else:
                self.text.set_text(self.text.text + event.unicode)
                self.pos_cursor[0] = min(self.pos_cursor[0] + 1, int(self.rect.width / self.char))
            if self.text.rect.width >= self.rect.width:
                self.pos[0] = self.rect.width - self.text.rect.width
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
            print(self.text.width // self.char - self.pos_cursor[0])
            pg.draw.rect(
                display, pg.Color(self.font_color),
                (
                    self.rect.x + self.pos_cursor[0] * self.char + int(round(self.text.rect.height / 10, 0)),
                    self.rect.y + self.text.rect.y,
                    int(round(self.text.rect.height / 10, 0)), self.rect.height
                )
            )
