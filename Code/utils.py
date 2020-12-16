from typing import Tuple

import pygame as pg


def print_text(display, text: str, pos: Tuple[int, int], font_color: Tuple[int, int, int] = (255, 0, 0),
               font_size: int = 20) -> None:
    font_type = pg.font.Font(None, font_size)
    text = font_type.render(text, True, font_color)
    text_rect = text.get_rect()
    display.blit(text, text_rect)


def max_size_font(text: str, width: int, height: int, font_type: str = None,
                  font_color: Tuple[int, int, int] = (255, 0, 0), font_size: int = 20):
    font_type_ = pg.font.Font(font_type, font_size)
    text_ = font_type_.render(text, True, font_color)
    w, h = text_.get_rect()
    while width > w and height > h:
        font_size += 1
        font_type_ = pg.font.Font(font_type, font_size)
        text_ = font_type_.render(text, True, font_color)
        w, h = text_.get_rect()
    return text_


class Text:
    def __init__(self, text: str, pos: Tuple[int, int], font_color: Tuple[int, int, int] = (255, 255, 255),
                 font_type: str = None, font_size: int = 20) -> None:
        self.font_type = pg.font.Font(font_type, font_size)
        self.surface = max_size_font()
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = pos
