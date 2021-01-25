import time
from Code.settings import *


class Processor:
    def __init__(self, sector, tick_complete=0, tick=0) -> None:
        self.tick_complete = tick_complete
        self.tick = tick
        self.time_update = 0.5  # 2 раза за секунду
        self.day = True
        self.sector = sector
        self.state = True

    def get_state(self) -> int:
        return 1 if self.state else 0

    def change(self) -> None:
        self.state = not self.state

    def ticked(self) -> None:
        t = time.time()
        if t - self.tick >= self.time_update:
            self.tick = t
            self.tick_complete += 1
            self.update()
        if self.tick_complete % UPDATE_CHANGE_TIME:
            self.day = not self.day

    def update(self) -> None:
        self.sector.update(self.tick_complete)
