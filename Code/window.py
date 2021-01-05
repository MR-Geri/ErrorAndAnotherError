from Code import settings
from Code.escape_menu import EscMenu
from Code.interface_utils import Interface
from Code.line_input import LineInput
from Code.settings import *

from typing import Tuple
import pygame as pg

from Code.Graphics.matrix import Matrix
from Code.sound import Sound
from Code.сamera import Camera
from Code.buttons import Button, Buttons, ButtonTwoStates
from Code.Map.sector import Sector
from Code.info_panel import LeftPanel, RightPanel
from Code.texts import max_size_list_text, TextCenter
from Code.slider import Slider, Sliders
from Code.sector_objects.robots import Robot


class Window:
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        self.caption = caption
        self.is_run = False
        self.last_window = None
        self.controller = controller
        self.volume = self.controller.volume
        self.music = self.controller.music
        self.win_width, self.win_height = size_display
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

    def draw(self) -> None:
        pass

    def update(self) -> None:
        pass

    def run(self, last: str = None) -> None:
        self.last_window = last
        pg.event.clear()
        self.is_run = True
        while self.is_run:
            self.clock.tick(FPS)
            self.display.blit(self.bd, (0, 0))
            self.event()
            self.draw()
            self.update()
            #
            pg.display.update()

    def join(self) -> None:
        self.is_run = False


class MenuWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super(MenuWindow, self).__init__(controller, size_display, caption)
        width3 = int(round(self.win_width / 3, 0))
        self.interface = Interface(
            pos=(self.win_width // 100, self.win_height // 6 + self.win_height // 100), max_width=self.win_width,
            max_height=self.win_height,
            indent=(0, self.win_height // 100), size=(width3, self.win_height // 10)
        )
        self.background = Matrix(
            (width3 + 2 * self.interface.x, self.interface.y),
            2 * width3 - self.interface.x - 2 * self.interface.x,
            2 * (self.win_height // 3), MENU_BACKGROUND
        )
        #
        self.buttons = Buttons()
        self.init_button()
        self.interface.move(0)
        #
        self.running_line = RunningLineMaxSizeCenter(
            text='тестовая строка', width=self.interface.width,
            height=self.background.rect.y + self.background.rect.height - self.interface.y,
            pos=self.interface.pos, speed=30, font_type=PT_MONO
        )
        self.music.play()
        #

    def init_button(self) -> None:
        width, height = self.interface.width, self.interface.height
        width3 = int(round(width / 3, 0))
        data = [('Новая игра', self.new_game), ('Загрузить игру', self.load_game), ('Настройки', self.settings),
                ('Выйти', self.exit)]
        size = max_size_list_text(
            ['Новая игра', 'Загрузить игру', 'Настройки', 'Выйти'], width, height, PT_MONO
        )
        for text, func in data:
            button = Button(
                pos=self.interface.pos, width=width, height=height, func=func,
                color_disabled=(30, 30, 30), color_active=(40, 40, 40),
                text=TextCenter(text=text, width=width, height=height, font_type=PT_MONO, font_size=size)
            )
            self.buttons.add(button)
            self.interface.move(0)
        button = Button(
            pos=self.interface.pos, width=width3, height=height, func=self.music.previous,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='<', width=width3, height=height, font_type=PT_MONO, font_size=size)
        )
        self.buttons.add(button)
        self.interface.move(button.rect.width, 0, is_indent=(False, False))
        button = ButtonTwoStates(
            pos=self.interface.pos, width=width - 2 * width3, height=self.interface.height,
            func=self.music.pause_and_play, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='||', width=width - 2 * width3, height=self.interface.height,
                            font_type=PT_MONO, font_size=size),
            texts=('►', '||'), get_state=self.music.get_state
        )
        self.buttons.add(button)
        self.interface.move(button.rect.width, 0, is_indent=(False, False))
        button = Button(
            pos=self.interface.pos, width=width3, height=height, func=self.music.next,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='>', width=width3, height=height, font_type=PT_MONO, font_size=size)
        )
        self.buttons.add(button)
        self.interface.move(- width + width3, 0, is_indent=(False, False))

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

    def draw(self) -> None:
        self.background.draw(self.display)  # матрица
        self.buttons.draw(self.display)
        self.running_line.draw(self.display)

    def update(self) -> None:
        pg.display.set_caption(str(self.clock.get_fps()))  # нужно для отладки. FPS в заголовок окна!
        self.running_line.update(self.music.get_text())
        self.buttons.update_text()

    def event(self) -> None:
        for en in pg.event.get():
            self.buttons.event(en)
            if en.type == pg.QUIT:
                pg.quit()
                quit()


class SettingsWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super().__init__(controller, size_display, caption)
        self.sliders = Sliders()
        self.init_sliders()
        self.input = LineInput(pos=(100, 140), width=500, height=30, font_type=PT_MONO, background_color='#000000')
        #

    def init_sliders(self) -> None:
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

    def draw(self) -> None:
        self.sliders.draw(self.display)
        self.input.draw(self.display)

    def event(self) -> None:
        for en in pg.event.get():
            self.sliders.event(en)
            self.input.event(en)
            if en.type == pg.KEYUP and en.key == pg.K_SPACE:
                self.controller.all_off()
                self.controller.init((1280, 720))
                self.controller.menu.run()
            if en.type == pg.QUIT:
                pg.quit()
                quit()
            if en.type == pg.KEYUP and en.key == pg.K_ESCAPE:
                self.controller.action_window(self.last_window)


class GameWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super().__init__(controller, size_display, caption)
        self.size_cell = CELL_SIZE
        # sector нужно ЗАГРУЖАТЬ если это НЕ НОВАЯ игра
        self.sound = Sound()
        self.sector = Sector(number_x=SECTOR_X_NUMBER, number_y=SECTOR_Y_NUMBER,
                             size_cell=self.size_cell, sound=self.sound)
        panel_width = self.win_width // INFO_PANEL_K
        self.left_panel = LeftPanel(panel_width, self.win_height, pos=(0, 0), music=self.music)
        self.right_panel = RightPanel(panel_width, self.win_height, pos=(self.win_width - panel_width, 0))
        self.camera = Camera(
            SECTOR_X_NUMBER * self.size_cell,
            SECTOR_Y_NUMBER * self.size_cell,
            self.left_panel.rect.width,
            self.left_panel.rect.width,
            self.win_width,
            self.win_height
        )
        self.esc_menu = EscMenu(pos=(self.win_width // 4, self.win_height // 4), width=self.win_width // 2,
                                height=self.win_height // 2, controller=self.controller)
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
                self.left_panel.rect.width,
                self.left_panel.rect.width,
                self.win_width,
                self.win_height
            )

    def get_number_cell(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = self.camera.get_cord()
        return int((-x + mouse_pos[0]) // self.size_cell), int((-y + mouse_pos[1]) // self.size_cell)

    def click(self, pos) -> None:
        if self.right_panel.rect.x > pos[0] > self.left_panel.rect.width:
            x, y = self.get_number_cell(pos)
            print('Клик по полю:\n', x, y)
        if pos[0] < self.left_panel.rect.width:
            print('Клик по левой панели информации.')
        if pos[0] > self.right_panel.rect.x:
            print('Клик по правой панели информации')

    def draw(self) -> None:
        self.left_panel.render()
        self.right_panel.render()
        #
        self.sector.draw(self.display, self.camera.get_cord())
        self.left_panel.draw(self.display)
        self.right_panel.draw(self.display)
        self.esc_menu.draw(self.display)

    def update(self) -> None:
        pg.display.set_caption(str(self.clock.get_fps()))  # нужно для отладки. FPS в заголовок окна!
        if not self.esc_menu.if_active:
            self.camera.move(self.camera_left, self.camera_right, self.camera_up, self.camera_down)
            #
            self.sound.play()
            # Обновление панели каждую секунду
            self.right_panel.update()
            self.left_panel.update()

    def read_file(self) -> None:
        sector = self.sector
        with open(PLAYER_CODE + 'main.py') as commands:
            try:
                r = commands.read().split('\n')
                for t in r:
                    try:
                        eval(str(t))
                    except SyntaxError:
                        exec(str(t))
                    except Exception as e:
                        print(e)
                self.sector.render()
            except Exception as e:
                print(e)

    def event(self) -> None:
        for en in pg.event.get():
            if en.type == pg.QUIT:
                pg.quit()
                quit()
            if en.type == pg.KEYUP and en.key == pg.K_ESCAPE:
                self.esc_menu.changes_active()
            if self.esc_menu.if_active:
                self.esc_menu.event(en)
            else:
                self.left_panel.event(en)
                self.right_panel.event(en)
                if en.type == pg.MOUSEBUTTONUP and en.button == 1:
                    self.click(pos=en.pos)
                if en.type == pg.MOUSEBUTTONUP and en.button == 3:
                    self.read_file()
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
