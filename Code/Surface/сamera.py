import pygame as pg
from Code.settings import *


class Camera(object):
    def __init__(self, camera_func, width, height) -> None:
        self.camera_func = camera_func
        self.state = pg.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect) -> pg.Rect:
    left, right, _, _ = target_rect
    _, _, w, h = camera
    left, right = -left + WIN_WIDTH / 2, -right + WIN_HEIGHT / 2

    left = min(0, left)                              # Не движемся дальше левой границы
    left = max(-(camera.width-WIN_WIDTH), left)      # Не движемся дальше правой границы
    right = max(-(camera.height-WIN_HEIGHT), right)  # Не движемся дальше нижней границы
    right = min(0, right)                            # Не движемся дальше верхней границы

    return pg.Rect(left, right, w, h)
