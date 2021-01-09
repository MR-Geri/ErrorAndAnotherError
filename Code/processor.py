from Code.settings import *

import pygame as pg


class Processor:
    def __init__(self) -> None:
        self.tick_complete = 0
        self.tick = 0
        self.tick_update = int(round(FPS / CHANGE_TICK, 0))  # 2 раза за секунду
        self.day = True

    def ticked(self) -> None:
        self.tick = (self.tick + 1) % (CHANGE_TICK + 1)
        if self.tick == self.tick_update:
            self.tick_complete += 1
            self.update()
        if self.tick_complete % UPDATE_CHANGE_TIME:
            self.day = not self.day

    def update(self) -> None:
        pass
