from typing import Tuple

import pygame as pg
from Code.settings import *


class Camera(object):
    def __init__(self, width: int, height: int, left: int, right: int) -> None:
        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.rect = pg.Rect((WIN_WIDTH - self.width) // 2, (WIN_HEIGHT - self.height) // 2, width, height)
        self.speed_x, self.speed_y = 0, 0

    def get_cord(self) -> Tuple[int, int]:
        return self.rect.x, self.rect.y

    def move(self, left: bool, right: bool, up: bool, down: bool) -> None:
        self.speed_x, self.speed_y = 0, 0
        max_width, max_height = WIN_WIDTH - self.width, WIN_HEIGHT - self.height
        if left:
            self.speed_x += CAMERA_SPEED_X
        if right:
            self.speed_x -= CAMERA_SPEED_X
        if up:
            self.speed_y += CAMERA_SPEED_Y
        if down:
            self.speed_y -= CAMERA_SPEED_Y
        if -max_width + self.left >= -(self.rect.x + self.speed_x) >= -self.left:
            self.rect.x += self.speed_x
        if -max_height >= -(self.rect.y + self.speed_y) >= 0:
            self.rect.y += self.speed_y
