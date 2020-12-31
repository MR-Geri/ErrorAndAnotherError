from Code.interface_utils import Interface
from Code.settings import *

from typing import Tuple
import pygame as pg

from Code.Graphics.matrix import Matrix
from Code.сamera import Camera
from Code.buttons import Button, Buttons, ButtonTwoStates
from Code.Map.sector import Sector
from Code.info_panel import LeftPanel, RightPanel
from Code.texts import max_size_list_text, TextCenter
from Code.slider import Slider, Sliders


class Window:
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        self.caption = caption
        self.is_run = False
        self.controller = controller
        self.volume = self.controller.volume
        self.music = self.controller.music
        #
        if FULL_SCREEN:
            self.display = pg.display.set_mode(size_display, pg.FULLSCREEN)
        else:
            self.display = pg.display.set_mode(size_display)
        pg.display.set_caption(self.caption)
        self.bd = pg.Surface(size_display)
        self.bd.fill(pg.Color(COLOR_BACKGROUND))
        #
        self.clock = CLOCK

    def event(self) -> None:
        for en in pg.event.get():
            if en.type == pg.QUIT:
                pg.quit()
                quit()

    def render(self) -> None:
        pass

    def update(self) -> None:
        pass

    def run(self) -> None:
        pg.event.clear()
        self.is_run = True
        while self.is_run:
            self.clock.tick(FPS)
            self.display.blit(self.bd, (0, 0))
            self.event()
            self.render()
            self.update()
            #
            pg.display.update()

    def join(self) -> None:
        self.is_run = False


class MenuWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super(MenuWindow, self).__init__(controller, size_display, caption)
        self.background = Matrix((0, 0), WIN_WIDTH, WIN_HEIGHT, MENU_BACKGROUND)
        #
        self.interface = Interface(
            pos=(WIN_WIDTH // 100, WIN_HEIGHT // 100), max_width=WIN_WIDTH, max_height=WIN_HEIGHT,
            indent=(0, WIN_HEIGHT // 100), size=(WIN_WIDTH // 3, WIN_HEIGHT // 10)
        )
        self.buttons = Buttons()
        self.init_button()
        #
        self.running_line = RunningLineMaxSizeCenter(
            text='тестовая строка', width=self.interface.width, height=self.interface.height,
            pos=self.interface.pos, speed=30, font_type=PT_MONO
        )
        self.music.play()
        #

    def init_button(self) -> None:
        width, height = self.interface.width, self.interface.height
        size = max_size_list_text(
            ['Новая игра', 'Загрузить игру', 'Настройки', 'Выйти'], width, height, PT_MONO
        )
        button = Button(
            pos=self.interface.pos, width=width, height=height, func=self.new_game,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='Новая игра', width=width, height=height, font_type=PT_MONO, font_size=size)
        )
        self.buttons.add(button)
        self.interface.move(0)
        button = Button(
            pos=self.interface.pos, width=width, height=height, func=self.load_game,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='Загрузить игру', width=width, height=height, font_type=PT_MONO, font_size=size)
        )
        self.buttons.add(button)
        self.interface.move(0)
        button = Button(
            pos=self.interface.pos, width=width, height=height, func=self.settings,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='Настройки', width=width, height=height, font_type=PT_MONO, font_size=size)
        )
        self.buttons.add(button)
        self.interface.move(0)
        button = Button(
            pos=self.interface.pos, width=width, height=height, func=self.exit,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='Выйти', width=width, height=height, font_type=PT_MONO, font_size=size)
        )
        self.buttons.add(button)
        self.interface.move(0)
        button = Button(
            pos=self.interface.pos, width=width // 3, height=height, func=self.music.previous,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='<', width=width // 3, height=height, font_type=PT_MONO, font_size=size)
        )
        self.buttons.add(button)
        self.interface.move(width // 3, 0, is_indent=(False, False))
        button = ButtonTwoStates(
            pos=self.interface.pos, width=self.interface.width // 3, height=self.interface.height,
            func=self.music.pause_and_play, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='||', width=self.interface.width // 3, height=self.interface.height,
                            font_type=PT_MONO, font_size=size),
            texts=('►', '||'), get_state=self.music.get_state
        )
        self.buttons.add(button)
        self.interface.move(width // 3, 0, is_indent=(False, False))
        button = Button(
            pos=self.interface.pos, width=width // 3, height=height, func=self.music.next,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='>', width=width // 3, height=height, font_type=PT_MONO, font_size=size)
        )
        self.buttons.add(button)
        self.interface.move(- 2 * (width // 3), is_indent=(False, True))

    def new_game(self) -> None:
        print('Новая игра')
        self.controller.action_window('game')

    def load_game(self) -> None:
        print('Загрузка игры')
        self.controller.action_window('game')

    def settings(self) -> None:
        print('Настройки')
        self.controller.action_window('settings')

    @staticmethod
    def exit() -> None:
        pg.quit()
        quit()

    def render(self) -> None:
        self.background.render(self.display)  # матрица
        self.buttons.render(self.display)
        self.running_line.render(self.display)

    def update(self) -> None:
        pg.display.set_caption(str(self.clock.get_fps()))  # нужно для отладки. FPS в заголовок окна!
        self.running_line.update(self.music.get_text())
        self.buttons.update_text()

    def event(self) -> None:
        for en in pg.event.get():
            self.buttons.update(en)
            if en.type == pg.QUIT:
                pg.quit()
                quit()


class SettingsWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super().__init__(controller, size_display, caption)
        self.sliders = Sliders()
        self.init_slider()
        #

    def init_slider(self) -> None:
        volume_slider = Slider(
            pos=(100, 100), width=500, height=30,
            color_no_use=COLOR_SLIDER_NO_USE,
            color_use=COLOR_SLIDER_USE,
            color_circle=COLOR_SLIDER_CIRCLE,
            slider=self.volume,
            func=self.music
        )
        self.sliders.add(volume_slider)

    def update(self) -> None:
        pg.display.set_caption(str(self.clock.get_fps()))  # нужно для отладки. FPS в заголовок окна!

    def render(self) -> None:
        self.sliders.render(self.display)

    def event(self) -> None:
        for en in pg.event.get():
            self.sliders.update(en)
            if en.type == pg.QUIT:
                pg.quit()
                quit()
            if en.type == pg.KEYUP and en.key == pg.K_ESCAPE:
                self.controller.action_window('menu')


class GameWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super().__init__(controller, size_display, caption)
        self.size_cell = CELL_SIZE
        # sector нужно ЗАГРУЖАТЬ если это НЕ НОВАЯ игра
        self.sector = Sector(number_x=SECTOR_X_NUMBER, number_y=SECTOR_Y_NUMBER, size_cell=self.size_cell)
        self.left_panel = LeftPanel(INFO_PANEL_WIDTH, WIN_HEIGHT, pos=(0, 0), music=self.music)
        self.right_panel = RightPanel(INFO_PANEL_WIDTH, WIN_HEIGHT, pos=(WIN_WIDTH - INFO_PANEL_WIDTH, 0))
        self.camera = Camera(
            SECTOR_X_NUMBER * self.size_cell,
            SECTOR_Y_NUMBER * self.size_cell,
            INFO_PANEL_WIDTH,
            INFO_PANEL_WIDTH
        )
        #
        self.camera_left, self.camera_right, self.camera_up, self.camera_down = False, False, False, False
        self.l_ctrl = False

    def scale(self, coeff_scale: float):
        # Масштабирование sector с ограничениями
        if (coeff_scale > 0 and self.size_cell < CELL_MAX_SIZE) or (coeff_scale < 0 and self.size_cell > CELL_MIN_SIZE):
            self.size_cell += coeff_scale
            self.sector.scale(self.size_cell)
            # Ограничение перемещения камеры|СОЗДАЁМ ЗАНОВО
            self.camera = Camera(
                SECTOR_X_NUMBER * self.size_cell,
                SECTOR_Y_NUMBER * self.size_cell,
                INFO_PANEL_WIDTH,
                INFO_PANEL_WIDTH
            )

    def get_number_cell(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = self.camera.get_cord()
        return int((-x + mouse_pos[0]) // self.size_cell), int((-y + mouse_pos[1]) // self.size_cell)

    def click(self, pos) -> None:
        if self.right_panel.rect.x > pos[0] > INFO_PANEL_WIDTH:
            x, y = self.get_number_cell(pos)
            print('Клик по полю:\n', x, y)
        if pos[0] < INFO_PANEL_WIDTH:
            print('Клик по левой панели информации.')
        if pos[0] > self.right_panel.rect.x:
            print('Клик по правой панели информации')

    def render(self) -> None:
        self.left_panel.render()
        self.right_panel.render()
        #
        self.display.blit(self.sector.surface, self.camera.get_cord())
        self.display.blit(self.left_panel.surface, self.left_panel.rect)
        self.display.blit(self.right_panel.surface, self.right_panel.rect)

    def update(self) -> None:
        pg.display.set_caption(str(self.clock.get_fps()))  # нужно для отладки. FPS в заголовок окна!
        self.camera.move(self.camera_left, self.camera_right, self.camera_up, self.camera_down)
        # Обновление панели каждую секунду
        self.right_panel.update()
        self.left_panel.update()

    def event(self) -> None:
        for en in pg.event.get():
            self.left_panel.event(en)
            self.right_panel.event(en)
            if en.type == pg.QUIT:
                pg.quit()
                quit()
            if en.type == pg.MOUSEBUTTONUP and en.button == 1:
                self.click(pos=en.pos)
            if en.type == pg.KEYUP and en.key == pg.K_ESCAPE:
                self.controller.action_window('menu')
            #
            if en.type == pg.KEYDOWN and en.key == pg.K_LCTRL:
                self.l_ctrl = True
            if en.type == pg.KEYUP and en.key == pg.K_LCTRL:
                self.l_ctrl = False
            #
            if self.l_ctrl and en.type == pg.MOUSEBUTTONUP and en.button == 4:
                self.scale(COEFFICIENT_SCALE)
            if self.l_ctrl and en.type == pg.MOUSEBUTTONUP and en.button == 5:
                self.scale(-COEFFICIENT_SCALE)
            #
            if en.type == pg.KEYDOWN and en.key == pg.K_w:
                self.camera_up = True
            if en.type == pg.KEYDOWN and en.key == pg.K_s:
                self.camera_down = True
            if en.type == pg.KEYDOWN and en.key == pg.K_d:
                self.camera_right = True
            if en.type == pg.KEYDOWN and en.key == pg.K_a:
                self.camera_left = True
            #
            if en.type == pg.KEYUP and en.key == pg.K_w:
                self.camera_up = False
            if en.type == pg.KEYUP and en.key == pg.K_s:
                self.camera_down = False
            if en.type == pg.KEYUP and en.key == pg.K_d:
                self.camera_right = False
            if en.type == pg.KEYUP and en.key == pg.K_a:
                self.camera_left = False
