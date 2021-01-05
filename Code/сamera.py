from Code.settings import *

from typing import Tuple
import pygame as pg


class Camera:
    def __init__(self, width: int, height: int, left: int, right: int, win_width: int, win_height: int) -> None:
        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.win_width, self.win_height = win_width, win_height
        self.rect = pg.Rect((self.win_width - self.width) // 2, (self.win_height - self.height) // 2, width, height)
        self.speed_x, self.speed_y = 0, 0

    def get_cord(self) -> Tuple[int, int]:
        return self.rect.x, self.rect.y

    def move(self, left: bool, right: bool, up: bool, down: bool) -> None:
        self.speed_x, self.speed_y = 0, 0
        max_width, max_height = self.win_width - self.width, self.win_height - self.height
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
