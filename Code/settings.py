from typing import Union
from os import walk


# Настройки окна
WIN_WIDTH, WIN_HEIGHT = 1920 // 2, 1080 // 2
DISPLAY_SIZE = (WIN_WIDTH, WIN_HEIGHT)
FULL_SCREEN = False
MENU_TITLE = 'Название игры'
FPS = 60
# Цвета
COLOR_BACKGROUND = '#313335'
COLOR_CELL = '#013a33'
COLOR_SLIDER_USE = '#25B2B9'
COLOR_SLIDER_NO_USE = '#D5F0F8'
COLOR_SLIDER_CIRCLE = 'white'
# Камера
CAMERA_SPEED_X, CAMERA_SPEED_Y = 2, 2
# Ячейки
COEFFICIENT_SCALE = 5
CELL_SIZE = 10  # Стартовое значение мастаба (MIN ZOOM)
CELL_MIN_SIZE = 10  # Нужно для масштабирования (ZOOM)
CELL_MAX_SIZE = 50  # Нужно для масштабирования (ZOOM)
SECTOR_Y_NUMBER = 50  # Размер сектора
SECTOR_X_NUMBER = 50  # Размер сектора
#
INFO_PANEL_WIDTH = WIN_WIDTH // 5
# Типизация
from Code.running_line import RunningLineMaxSizeCenter
from Code.Map.cell import Plain, Swamp, Mountain
from Code.texts import Text, TextMaxSize, TextMaxSizeCenter, TextCenter
ALL_TEXT = Union[Text, TextMaxSize, TextMaxSizeCenter, TextCenter]
ALL_RUNNING_LINE = Union[RunningLineMaxSizeCenter]
ALL_CELL = Union[Plain, Swamp, Mountain]
COLOR = Union[tuple, str]
# Font
PT_MONO = '../Data/Font/PT Mono.ttf'
MS_MINCHO = '../Data/Font/MS Mincho.ttf'
# Path
MENU_BACKGROUND = '../Data/Images/game.jpg'
# Биомы
MAX_SIZE_MOUNTAIN = (10, 10)
MAX_QUANTITY_MOUNTAIN = 3
MIN_QUANTITY_MOUNTAIN_CELL = 4
MAX_SIZE_SWAMP = (20, 20)
MAX_QUANTITY_SWAMP = 5
MIN_QUANTITY_SWAMP_CELL = 8
# Музыка
ALL_BACKGROUND_MUSIC = [[root + i for i in files] for root, _, files in walk('../Data/Sounds/background_music/')][0]
#
