import pygame as pg
from Code.window import MenuWindow
from Code.settings import *


if __name__ == '__main__':
    pg.init()
    menu = MenuWindow(DISPLAY_SIZE, MENU_TITLE)
    menu.run()
