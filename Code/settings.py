from typing import Union, Tuple
from os import walk
import pygame as pg
from random import randint


# Настройки окна
WIN_WIDTH, WIN_HEIGHT = 1280, 720
DISPLAY_SIZE = (WIN_WIDTH, WIN_HEIGHT)
FULL_SCREEN = False
MENU_TITLE = 'Название игры'
FPS = 60
UPDATE_CHANGE_TIME = 1440
CHANGE_TICK = 2
CLOCK = pg.time.Clock()
# Цвета
COLOR_BACKGROUND = '#313335'
COLOR_CELL = '#013a33'
COLOR_SLIDER_USE = '#25B2B9'
COLOR_SLIDER_NO_USE = '#D5F0F8'
COLOR_SLIDER_CIRCLE = 'white'
# Камера
MAX_SCALE = 5
CAMERA_K_SPEED_X, CAMERA_K_SPEED_Y = 5, 5
# Ячейки
SECTOR_Y_NUMBER = 50  # Размер сектора
SECTOR_X_NUMBER = 50  # Размер сектора
#
INFO_PANEL_K = 5
# Path
PT_MONO = '../Data/Font/PT Mono.ttf'
MS_MINCHO = '../Data/Font/MS Mincho.ttf'

MENU_BACKGROUND = '../Data/Images/game.jpg'

PATH_CRASHES = '../Data/Sounds/crashes/'
PATH_MOVES = '../Data/Sounds/moves/'
PATH_CHARGE = '../Data/Sounds/charge/'
ALL_BACKGROUND_MUSIC = [[root + i for i in files] for root, _, files in walk('../Data/Sounds/background_music/')][0]

PLAYER_CODE = '../Game_code/'
SAVE = '../Data/Save/'
# Типизация
COLOR = Union[Tuple[int, int, int], str]
from Code.texts import Text, TextMaxSize, TextMaxSizeCenter, TextCenter
ALL_TEXT = Union[Text, TextMaxSize, TextMaxSizeCenter, TextCenter]
from Code.running_line import RunningLineMaxSizeCenter
ALL_RUNNING_LINE = Union[RunningLineMaxSizeCenter]
from Code.Map.cell import Plain, Swamp, Mountain
ALL_CELL = Union[Plain, Swamp, Mountain]
from Code.sector_objects.robots import MK0
ALL_ROBOT = Union[MK0]
#
from Code.buttons import Button, ButtonTwoStates, ChoiceButton
BUTTONS = [Button, ButtonTwoStates, ChoiceButton]
# Биомы
CELLS = {'Plain': Plain, 'Swamp': Swamp, 'Mountain': Mountain}
MAX_SIZE_MOUNTAIN = (10, 10)
MAX_QUANTITY_MOUNTAIN = 3
MIN_QUANTITY_MOUNTAIN_CELL = 4
MAX_SIZE_SWAMP = (20, 20)
MAX_QUANTITY_SWAMP = 5
MIN_QUANTITY_SWAMP_CELL = 8
SELL_BLOCKED = [Mountain]
#
from Code.sector_objects.bases import Base
ROBOTS = [MK0]
BASES = [Base]
#
