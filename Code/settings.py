from Code.texts import Text, TextMaxSize, TextMaxSizeCenter


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
CELL_Y_NUMBER = 50
CELL_X_NUMBER = 50
CELL_SIZE = 10
CELL_MIN_SIZE = 10
CELL_MAX_SIZE = 50
#
INFO_PANEL_WIDTH = WIN_WIDTH // 5
# Типизация
ALL_TEXT = Text or TextMaxSize or TextMaxSizeCenter
COLOR = str or tuple
# Font
PT_MONO = '../Data/Font/PT Mono.ttf'
MS_MINCHO = '../Data/Font/MS Mincho.ttf'
# Path
MENU_BACKGROUND = '../Data/game.jpg'
#
