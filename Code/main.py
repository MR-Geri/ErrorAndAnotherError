import pygame as pg

from Code.slider import Numbers
from Code.sound import Music
from Code.window import MenuWindow, SettingsWindow, GameWindow
from Code.settings import *


class Controller:
    def __init__(self) -> None:
        self.volume = Numbers(0, 1, 0.01)
        self.music = Music(path=ALL_BACKGROUND_MUSIC, volume=self.volume.value)
        #
        self.menu = MenuWindow(self, DISPLAY_SIZE, MENU_TITLE)
        self.settings = SettingsWindow(self, DISPLAY_SIZE, MENU_TITLE)
        self.game = GameWindow(self, DISPLAY_SIZE, MENU_TITLE)
        #
        self.windows = {'menu': self.menu, 'settings': self.settings, 'game': self.game}

    def action_window(self, window_act: str) -> None:
        for window in self.windows.keys() - [window_act]:
            self.windows[window].join()
        self.windows[window_act].run()


if __name__ == '__main__':
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()
    controller = Controller()
    controller.menu.run()
