import pyperclip

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
        self.l_ctrl = False
        self.if_active = False
        self.tick = 0
        #
        self.font_color = font_color
        self.font_type = font_type
        self.background_color = background_color
        #
        self.text = TextMaxSize('', width=None, height=height, font_color=font_color, font_type=font_type)
        self.char = TextMaxSize('F', width=None, height=height, font_color=font_color, font_type=font_type).rect.width
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.render()

    def clear(self) -> None:
        self.text = TextMaxSize('', width=None, height=self.rect.height, font_color=self.font_color,
                                font_type=self.font_type)
        self.pos = [0, 0]
        self.pos_cursor = [0, 0]
        self.if_active = False
        self.render()

    def event(self, event: pg.event.Event) -> None:
        """
        Я сам не знаю, что тут происходит.
        Если эта дичь не работает. ГОСПАДЕ перепиши сам по братски.
        СЯБ!
        """
        if event.type == pg.KEYDOWN and event.key == pg.K_LCTRL:
            self.l_ctrl = True
        if event.type == pg.KEYUP and event.key == pg.K_LCTRL:
            self.l_ctrl = False
        if event.type == pg.KEYDOWN and self.if_active:
            cur = int((-self.pos[0] / self.char) + self.pos_cursor[0])
            text = [self.text.text[:cur], self.text.text[cur:]]
            if event.key == pg.K_RETURN:
                self.if_active = False
                self.tick = 0
            elif event.key == pg.K_BACKSPACE or event.key == pg.K_LEFT:
                if event.key == pg.K_BACKSPACE:
                    self.text.set_text(text[0][:-1] + text[1])
                if self.pos_cursor[0] == 0 and self.pos[0] < 0:
                    self.pos[0] += self.char
                self.pos_cursor[0] = max(self.pos_cursor[0] - 1, 0)
            if event.key == pg.K_DELETE:
                self.text.set_text(text[0] + text[1][1:])
            elif event.key == pg.K_RIGHT or event.unicode:
                if event.unicode:
                    self.text.set_text(text[0] + event.unicode + text[1])
                if self.pos_cursor[0] >= int(self.rect.width / self.char) and -self.pos[0] <= self.text.rect.width - \
                        self.rect.width:
                    self.pos[0] -= self.char
                self.pos_cursor[0] = min(
                    self.pos_cursor[0] + 1, int(self.text.rect.width / self.char), int(self.rect.width / self.char))
            elif self.l_ctrl and event.key == pg.K_v:
                c_v = str(pyperclip.paste()).replace('\n', ' ')
                if c_v:
                    self.text.set_text(text[0] + c_v + text[1])
                if self.pos_cursor[0] >= int(self.rect.width / self.char) and -self.pos[0] <= self.text.rect.width - \
                        self.rect.width:
                    self.pos[0] -= self.char * len(c_v)
                self.pos_cursor[0] = min(
                    self.pos_cursor[0] + len(c_v),
                    int(self.text.rect.width / self.char), int(self.rect.width / self.char))
            self.render()
        try:
            if self.rect.collidepoint(*event.pos) and event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.if_active = True
                self.tick = 0
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.if_active = False
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
        if self.if_active and self.tick <= FPS:
            pg.draw.rect(
                display, pg.Color(self.font_color),
                (
                    self.rect.x + self.pos_cursor[0] * self.char + int(round(self.text.rect.height / 10, 0)),
                    self.rect.y + self.text.rect.y,
                    int(round(self.text.rect.height / 10, 0)), self.rect.height
                )
            )
