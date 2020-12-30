from typing import Tuple

import pygame as pg


def print_text(display, text: str, pos: Tuple[int, int], font_color: Tuple[int, int, int] = (255, 0, 0),
               font_size: int = 20) -> None:
    font_type = pg.font.Font(None, font_size)
    text = font_type.render(text, True, font_color)
    text_rect = text.get_rect()
    text_rect.x, text_rect.y = pos
    display.blit(text, text_rect)


def max_size_list_text(texts: list, width: int, height: int, font_type: str = None) -> int:
    size = list()
    for text in texts:
        size.append(TextMaxSize(text=text, width=width, height=height, font_type=font_type).font_size)
    return min(size)


class Text:
    def __init__(self, text: str, pos: Tuple[int, int] = (0, 0), font_color: Tuple[int, int, int] = (255, 255, 255),
                 font_type: str = None, font_size: int = 20) -> None:
        self.font_type = pg.font.Font(font_type, font_size)
        self.surface = self.font_type.render(text, True, font_color)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = pos


class TextMaxSize:
    def __init__(self, text: str,  pos: Tuple[int, int] = (0, 0), width: int = None, height: int = None,
                 font_color: Tuple[int, int, int] = (255, 255, 255), font_type: str = None) -> None:
        self.font_size = 1
        while True:
            self.surface = pg.font.Font(font_type, self.font_size).render(text, True, font_color)
            self.rect = self.surface.get_rect()
            if (width and width <= self.rect.width) or (height and height <= self.rect.height):
                self.font_size -= 1
                self.surface = pg.font.Font(font_type, self.font_size).render(text, True, font_color)
                self.rect = self.surface.get_rect()
                self.rect.x, self.rect.y = pos
                break
            self.font_size += 1


class TextMaxSizeCenter(TextMaxSize):
    def __init__(self, text: str, width: int = None, height: int = None, pos: Tuple[int, int] = (0, 0),
                 font_color: Tuple[int, int, int] = (255, 255, 255), font_type: str = None) -> None:
        super().__init__(text=text, pos=pos, width=width, height=height, font_color=font_color, font_type=font_type)
        if width:
            self.rect.x += (width - self.rect.width) // 2
        if height:
            self.rect.y += (height - self.rect.height) // 2


class TextCenter(Text):
    def __init__(self, text: str, width: int = None, height: int = None, pos: Tuple[int, int] = (0, 0),
                 font_color: Tuple[int, int, int] = (255, 255, 255),
                 font_type: str = None, font_size: int = 20) -> None:
        super().__init__(text=text, pos=pos, font_color=font_color, font_type=font_type, font_size=font_size)
        if width:
            self.rect.x += (width - self.rect.width) // 2
        if height:
            self.rect.y += (height - self.rect.height) // 2
