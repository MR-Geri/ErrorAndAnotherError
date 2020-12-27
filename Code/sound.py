import pygame as pg


class Music:
    def __init__(self, path: str, volume: int) -> None:
        self.path = path
        self.volume = volume
        self.set_music(self.path)

    def set_music(self, path: str) -> None:
        self.path = path
        pg.mixer.music.load(path)
