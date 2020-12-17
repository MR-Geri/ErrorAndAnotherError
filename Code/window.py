from typing import Tuple
import pygame as pg
import datetime

from Code.Surface.сamera import Camera
from Code.buttons import Button
from Code.settings import *
from Code.Surface.sector import Sector
from Code.info_panel import LeftPanel, RightPanel


class Window:
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        self.caption = caption
        self.is_run = False
        self.controller = controller
        #
        if FULL_SCREEN:
            self.display = pg.display.set_mode(size_display, pg.FULLSCREEN)
        else:
            self.display = pg.display.set_mode(size_display)
        pg.display.set_caption(self.caption)
        self.bd = pg.Surface(size_display)
        self.bd.fill(pg.Color(BACKGROUND_COLOR))
        #
        self.clock = pg.time.Clock()

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
        super().__init__(controller, size_display, caption)
        self.button = Button(
            pos=(10, 10), width=WIN_WIDTH // 5, height=WIN_HEIGHT // 10, func=self.ck,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextMaxSizeCenter(text='Играть', width=WIN_WIDTH // 5, height=WIN_HEIGHT // 10, font_type=PT_MONO)
        )

    def new_game(self) -> None:
        self.controller.action_window('game')

    def ck(self):
        print(123)

    def load_game(self) -> None:
        pass

    def settings(self) -> None:
        pass

    def render(self) -> None:
        self.display.blit(self.button.surface, self.button.rect)

    def update(self) -> None:
        pg.display.set_caption(str(self.clock.get_fps()))  # нужно для отладки. FPS в заголовок окна!

    def event(self) -> None:
        for en in pg.event.get():
            self.button.update(en)
            if en.type == pg.QUIT:
                pg.quit()
                quit()
            elif en.type == pg.KEYUP and en.key == pg.K_SPACE:
                self.new_game()


class SettingsWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super().__init__(controller, size_display, caption)


class GameWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super().__init__(controller, size_display, caption)
        self.size_cell = CELL_SIZE
        self.sector = Sector(width=CELL_X_NUMBER, height=CELL_Y_NUMBER, size_cell=self.size_cell)
        self.left_panel = LeftPanel(INFO_PANEL_WIDTH, WIN_HEIGHT, pos=(0, 0))
        self.right_panel = RightPanel(INFO_PANEL_WIDTH, WIN_HEIGHT, pos=(WIN_WIDTH - INFO_PANEL_WIDTH, 0))
        self.time_update_right_panel = datetime.datetime.now()
        self.camera = Camera(
            CELL_X_NUMBER * self.size_cell,
            CELL_Y_NUMBER * self.size_cell,
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
                CELL_X_NUMBER * self.size_cell,
                CELL_Y_NUMBER * self.size_cell,
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
        self.display.blit(self.sector.surface, self.camera.get_cord())
        self.display.blit(self.left_panel.surface, self.left_panel.rect)
        self.display.blit(self.right_panel.surface, self.right_panel.rect)

    def update(self) -> None:
        time_now = datetime.datetime.now()
        time_update_right_panel = time_now - self.time_update_right_panel
        #
        pg.display.set_caption(str(self.clock.get_fps()))  # нужно для отладки. FPS в заголовок окна!
        self.camera.move(self.camera_left, self.camera_right, self.camera_up, self.camera_down)
        # Обновление панели каждую секунду
        if int(time_update_right_panel.seconds) >= 1:
            self.time_update_right_panel = time_now
            self.right_panel.update()
            self.right_panel.render()

    def event(self) -> None:
        for en in pg.event.get():
            if en.type == pg.QUIT:
                pg.quit()
                quit()
            if en.type == pg.MOUSEBUTTONUP and en.button == 1:
                self.click(pos=en.pos)
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
