from Code.buttons import Buttons, Button, ButtonTwoStates
from Code.interface_utils import Interface
from Code.settings import *

from typing import Tuple
import pygame as pg
import datetime

from Code.sound import Music
from Code.texts import TextMaxSizeCenter, max_size_list_text


class Panel:
    def __init__(self, width: int, height: int, pos: Tuple[int, int]) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.color_background = pg.Color((128, 128, 128))
        self.interface = Interface(
            pos=(0, self.rect.height // 50), max_width=width, max_height=height,
            indent=(0, self.rect.height // 100), size=(self.rect.width, self.rect.height // 20)
        )

    def get_absolute_pos(self, x: int, y: int) -> Tuple[int, int]:
        return self.rect.x + x, self.rect.y + y

    def render(self) -> None:
        pass

    def update(self) -> None:
        pass

    def event(self, event: pg.event.Event) -> None:
        pass


class LeftPanel(Panel):
    def __init__(self, width: int, height: int, pos: Tuple[int, int], music: Music = None) -> None:
        super().__init__(width, height, pos)
        self.music = music
        # Интерфейс
        self.system_time = TextMaxSizeCenter(
            text=f"{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}", width=self.interface.width,
            height=self.interface.height, pos=self.interface.pos, font_type=PT_MONO
        )
        self.interface.move(0)
        self.running_line = RunningLineMaxSizeCenter(
            text='пример текста', width=self.interface.width, height=self.interface.height,
            pos=self.interface.pos, speed=30, font_type=PT_MONO
        )
        self.interface.move(0)
        self.buttons = Buttons()
        self.init_button()
        self.interface.move(0)
        #
        self.update()
        self.render()

    def init_button(self) -> None:
        size = max_size_list_text(
            ['<', '>', '||', '►'], self.interface.width, self.interface.height, PT_MONO
        )
        width3, height = int(round(self.interface.width / 3, 0)), 2 * self.interface.height + self.interface.indent[1]
        button = Button(
            pos=self.interface.pos, width=width3, height=height,
            func=self.music.previous, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(
                text='<', width=width3, height=height, font_type=PT_MONO,
                font_size=size
            )
        )
        self.buttons.add(button)
        self.interface.move(button.rect.width, 0, is_indent=(False, False))
        button = ButtonTwoStates(
            pos=self.interface.pos, width=self.interface.width - 2 * width3, height=height,
            func=self.music.pause_and_play, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='||', width=self.interface.width - 2 * width3, height=height,
                            font_type=PT_MONO, font_size=size),
            texts=('►', '||'), get_state=self.music.get_state
        )
        self.buttons.add(button)
        self.interface.move(button.rect.width, 0, is_indent=(False, False))
        button = Button(
            pos=self.interface.pos, width=width3, height=height,
            func=self.music.next, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(
                text='>', width=width3, height=height, font_type=PT_MONO,
                font_size=size
            )
        )
        self.buttons.add(button)
        self.interface.move(- self.interface.width, is_indent=(False, False))

    def update(self) -> None:
        self.running_line.update(self.music.get_text())
        self.system_time.set_text(f"{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
        self.buttons.update_text()

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(self.color_background)
        #
        self.running_line.render(self.surface)
        self.system_time.render(self.surface)
        self.buttons.render(self.surface)

    def event(self, event: pg.event.Event) -> None:
        self.buttons.update(event)


class RightPanel(Panel):
    def __init__(self, width: int, height: int, pos: Tuple[int, int]) -> None:
        super().__init__(width, height, pos)
        # Интерфейс
        #
        self.update()
        self.render()

    def update(self) -> None:
        pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill(self.color_background)
        #
