from typing import Tuple

import pygame as pg
from Code.settings import *


class Camera(object):
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.rect = pg.Rect(0, 0, width, height)
        self.speed_x, self.speed_y = 0, 0

    def get_cord(self) -> Tuple[int, int]:
        return self.rect.x, self.rect.y

    def move(self, left: bool, right: bool, up: bool, down: bool) -> None:
        self.speed_x, self.speed_y = 0, 0
        if left:
            self.speed_x += CAMERA_SPEED_X
        if right:
            self.speed_x -= CAMERA_SPEED_X
        if up:
            self.speed_y += CAMERA_SPEED_Y
        if down:
            self.speed_y -= CAMERA_SPEED_Y
        self.rect.x = -min(self.width - WIN_WIDTH, -min(0, self.rect.x + self.speed_x))    # Ограничение по X
        self.rect.y = -min(self.height - WIN_HEIGHT, -min(0, self.rect.y + self.speed_y))  # Ограничение по Y
