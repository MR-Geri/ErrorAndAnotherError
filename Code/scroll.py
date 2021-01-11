from Code.settings import *


class Scroll:
    def __init__(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.rect = pg.Rect()
