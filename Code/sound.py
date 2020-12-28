from typing import Union
from random import choice

import pygame as pg


class Music:
    def __init__(self, path: Union[str, list], volume: float = 0) -> None:
        self.is_play = None
        self.list_path = path if type(path) == list else None
        self.path = path if type(path) == str else choice(self.list_path)
        self.volume = volume
        self.set_music(self.path)

    def next(self) -> None:
        self.stop()
        self.set_music(self.list_path[(self.list_path.index(self.path) + 1) % len(self.list_path)])
        self.play()

    def previous(self) -> None:
        self.stop()
        ind = self.list_path.index(self.path)
        self.set_music(self.list_path[ind - 1 if ind > 0 else len(self.list_path) - 1])
        self.play()

    def set_music(self, path: str) -> None:
        self.path = path
        pg.mixer.music.load(path)
        pg.mixer.music.set_volume(self.volume)

    def update(self, volume: float) -> None:
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)

    def play(self) -> None:
        if self.is_play is None:
            pg.mixer.music.play(-1)
        elif not self.is_play:
            pg.mixer.music.unpause()
        self.is_play = True

    def stop(self) -> None:
        pg.mixer.music.stop()
        self.is_play = None

    def pause(self) -> None:
        self.is_play = False
        pg.mixer.music.pause()