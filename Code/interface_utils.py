from typing import Tuple


class InterfaceError(Exception):
    pass


class Interface:
    def __init__(self, pos: Tuple[int, int], max_width: int, max_height: int,
                 indent: Tuple[int, int], size: Tuple[int, int]):
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
        if self.pos[0] + width <= self.max_width:
            self.pos[0] += width
            self.pos[0] += self.indent[0] if is_indent[0] else 0
        else:
            raise InterfaceError("Выход за границы окна.")
        #
        if self.pos[1] + height <= self.max_height:
            self.pos[1] += height
            self.pos[1] += self.indent[1] if is_indent[1] else 0
        else:
            raise InterfaceError("Выход за границы окна.")
        #
        self.x, self.y = self.pos