from Code.settings import *
from Code.buttons import Button


class Scroll:
    def __init__(self, pos: Tuple[int, int], width: int, height: int, color: COLOR, if_button: bool = False,
                 color_disabled: COLOR = (30, 30, 30), color_active: COLOR = (40, 40, 40)) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.color = color
        self.surface.fill(self.color)
        self.if_button = if_button
        self.color_active = color_active
        self.color_disabled = color_disabled
        #
        self.lines = []

    def render(self, lines: list) -> None:
        self.surface.fill(self.color)
        self.lines = []
        for line in lines:
            if self.if_button:
                text, func = line
                self.lines.append(Button(text=text, pos=text.pos, width=text.width, height=text.height,
                                         color_active=self.color_active, color_disabled=self.color_disabled,
                                         func=func))
            else:
                self.lines.append(line)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)
        for line in self.lines:
            line.draw(surface)

    def event(self, event: pg.event.Event) -> None:
        for line in self.lines:
            if type(line) in BUTTONS:
                line.event(event)
