from typing import Tuple


class InterfaceError(Exception):
    pass


class Interface:
    def __init__(self, pos: Tuple[int, int], max_width: int = None, max_height: int = None,
                 indent: Tuple[int, int] = None, size: Tuple[int, int] = None):
        self.start_pos = pos
        self.pos = list(pos)
        self.x, self.y = self.pos
        self.max_width = max_width
        self.max_height = max_height
        self.indent = indent
        self.size = size
        self.width, self.height = self.size

    def move(self, width: int = None, height: int = None, is_indent: Tuple[bool, bool] = (True, True)):
        width = self.size[0] if width is None else width
        height = self.size[1] if height is None else height
        #
        if not self.max_width or self.pos[0] + width <= self.max_width + self.start_pos[0]:
            self.pos[0] += width
            self.pos[0] += self.indent[0] if is_indent[0] else 0
        else:
            raise InterfaceError("Выход за границы окна.")
        #
        if not self.max_height or self.pos[1] + height <= self.max_height + self.start_pos[1]:
            self.pos[1] += height
            self.pos[1] += self.indent[1] if is_indent[1] else 0
        else:
            raise InterfaceError("Выход за границы окна.")
        #
        self.x, self.y = self.pos


class Txt:
    def __init__(self, text: str) -> None:
        self.text = text

    def set_text(self, text: str) -> None:
        self.text = text
