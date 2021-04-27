import time
from Code.settings import *


class Processor:
    def __init__(self, sector, tick_complete=0, tick=0) -> None:
        self.tick_complete = tick_complete
        self.tick = tick
        self.time_update = 2  # 2 раза за секунду
        self.max_speed = 8
        self.min_speed = 1
        self.day = True
        self.sector = sector
        self.state = True

    def get_state(self) -> int:
        return 1 if self.state else 0

    def change(self) -> None:
        self.state = not self.state

    def up_speed(self) -> None:
        self.time_update = min(self.time_update + 1, self.max_speed)

    def down_speed(self) -> None:
        self.time_update = max(self.time_update - 1, self.min_speed)

    def ticked(self) -> None:
        t = time.time()
        if t - self.tick >= 1 / self.time_update:
            self.tick = t
            self.tick_complete += 1
            self.update()
            self.enemy_check()
        if self.tick_complete % UPDATE_CHANGE_TIME:
            self.day = not self.day

    def enemy_check(self) -> None:
        # Спавн базы противника
        if self.sector.enemy_base is None and self.tick_complete > UPDATE_CHANGE_TIME * 2:
            self.sector.place_enemy_base()
        if self.sector.enemy_base:
            self.sector.check_enemy(self.tick_complete)

    def update(self) -> None:
        self.sector.update(self.tick_complete)
