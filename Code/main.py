import pygame as pg
from Code.window import MenuWindow, SettingsWindow, GameWindow
from Code.settings import *


class Controller:
    def __init__(self):
        self.menu = MenuWindow(self, DISPLAY_SIZE, MENU_TITLE)
        self.settings = SettingsWindow(self, DISPLAY_SIZE, MENU_TITLE)
        self.game = GameWindow(self, DISPLAY_SIZE, MENU_TITLE)


if __name__ == '__main__':
    pg.init()
    controller = Controller()
    controller.menu.run()
