from Code.Map.cell import Plain, Swamp, Mountain
from Code.texts import Text, TextMaxSize, TextMaxSizeCenter, TextCenter

# Настройки окна
WIN_WIDTH, WIN_HEIGHT = 1920 // 2, 1080 // 2
DISPLAY_SIZE = (WIN_WIDTH, WIN_HEIGHT)
FULL_SCREEN = False
MENU_TITLE = 'Название игры'
FPS = 60
# Цвета
BACKGROUND_COLOR = '#313335'
CELL_COLOR = '#013a33'
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
ALL_TEXT = Text or TextMaxSize or TextMaxSizeCenter or TextCenter
ALL_CELL = Plain or Swamp or Mountain
COLOR = str or tuple
# Font
PT_MONO = '../Data/Font/PT Mono.ttf'
MS_MINCHO = '../Data/Font/MS Mincho.ttf'
# Path
MENU_BACKGROUND = '../Data/game.jpg'
# Биомы
MAX_SIZE_MOUNTAIN = (20, 20)
MAX_QUANTITY_MOUNTAIN = 1
MIN_QUANTITY_MOUNTAIN_CELL = 4
#
