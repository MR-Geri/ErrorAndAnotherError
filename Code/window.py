import pygame as pg
from typing import Tuple

from Code.Surface.сamera import Camera
from Code.settings import *
from Code.Surface.sector import Sector


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
        self.size_cell = SIZE_CELL
        self.sector = Sector(width=100, height=100, size_cell=self.size_cell)
        self.camera = Camera(100 * self.size_cell, 100 * self.size_cell)
        self.camera_left, self.camera_right, self.camera_up, self.camera_down = False, False, False, False
        self.l_ctrl = False

    def render(self) -> None:
        pg.display.set_caption(str(self.clock.get_fps()))  # нужно для отладки. FPS в заголовок окна!
        self.display.blit(self.sector.surface, self.camera.get_cord())

    def scale(self):
        # Масштабирование sector
        self.size_cell *= 1.1
        self.sector.scale(self.size_cell)
        #

    def get_number_cell(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = self.camera.get_cord()
        return (-x + mouse_pos[0]) // self.size_cell, (-y + mouse_pos[1]) // self.size_cell

    def event(self) -> None:
        for en in pg.event.get():
            if en.type == pg.QUIT:
                pg.quit()
                quit()
            if en.type == pg.MOUSEBUTTONUP and en.button == 1:
                print(self.get_number_cell(en.pos))
            #
            if en.type == pg.KEYDOWN and en.key == pg.K_LCTRL:
                self.l_ctrl = True
            if en.type == pg.KEYUP and en.key == pg.K_LCTRL:
                self.l_ctrl = False
            #
            if self.l_ctrl and en.type == pg.MOUSEBUTTONUP and en.button == 4:
                print('вверх')
            if self.l_ctrl and en.type == pg.MOUSEBUTTONUP and en.button == 5:
                print('вниз')
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
