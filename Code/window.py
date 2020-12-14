import pygame as pg
from typing import Tuple

from Code.Surface.сamera import Camera
from Code.settings import *
from Code.Surface.sector import Sector
from Code.info_panel import InfoPanels


class Window:
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        self.caption = caption
        self.is_run = False
        self.controller = controller
        #
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

    def run(self) -> None:
        self.is_run = True
        while self.is_run:
            self.clock.tick(FPS)
            self.display.blit(self.bd, (0, 0))
            self.event()
            self.render()
            #
            pg.display.update()

    def join(self) -> None:
        self.is_run = False


class MenuWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super().__init__(controller, size_display, caption)

    def event(self) -> None:
        for en in pg.event.get():
            if en.type == pg.QUIT:
                pg.quit()
                quit()
            elif en.type == pg.KEYUP and en.key == pg.K_SPACE:
                self.controller.action_window('game')


class SettingsWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super().__init__(controller, size_display, caption)


class GameWindow(Window):
    def __init__(self, controller: object, size_display: Tuple[int, int], caption: str) -> None:
        super().__init__(controller, size_display, caption)
        self.size_cell = CELL_SIZE
        self.sector = Sector(width=CELL_X_NUMBER, height=CELL_Y_NUMBER, size_cell=self.size_cell)
        self.panel = InfoPanels(INFO_PANEL_X, WIN_HEIGHT)
        self.camera = Camera(
            CELL_X_NUMBER * self.size_cell,
            CELL_Y_NUMBER * self.size_cell,
            self.panel.width,
            self.panel.width
        )
        #
        self.camera_left, self.camera_right, self.camera_up, self.camera_down = False, False, False, False
        self.l_ctrl = False

    def render(self) -> None:
        pg.display.set_caption(str(self.clock.get_fps()))  # нужно для отладки. FPS в заголовок окна!
        self.display.blit(self.sector.surface, self.camera.get_cord())
        self.display.blit(self.panel.panel_left, self.panel.panel_left_cord)
        self.display.blit(self.panel.panel_right, self.panel.panel_right_cord)

    def scale(self, coeff_scale: float):
        # Масштабирование sector с ограничениями
        if (coeff_scale > 0 and self.size_cell < CELL_MAX_SIZE) or (coeff_scale < 0 and self.size_cell > CELL_MIN_SIZE):
            self.size_cell += coeff_scale
            self.sector.scale(self.size_cell)
            # Ограничение перемещения камеры|СОЗДАЁМ ЗАНОВО
            self.camera = Camera(
                CELL_X_NUMBER * self.size_cell,
                CELL_Y_NUMBER * self.size_cell,
                self.panel.width,
                self.panel.width
            )

    def get_number_cell(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = self.camera.get_cord()
        return int((-x + mouse_pos[0]) // self.size_cell), int((-y + mouse_pos[1]) // self.size_cell)

    def click(self, pos) -> None:
        if self.panel.panel_right_cord[0] > pos[0] > self.panel.width:
            x, y = self.get_number_cell(pos)
            print('Клик по полю:\n', x, y)
        if pos[0] < self.panel.width:
            print('Клик по левой панели информации.')
        if pos[0] > self.panel.panel_right_cord[0]:
            print('Клик по правой панели информации')

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

        self.camera.move(self.camera_left, self.camera_right, self.camera_up, self.camera_down)
