from Code.interface_utils import Interface
from Code.settings import *
from Code.buttons import ChoiceButton


class Scroll:
    def __init__(self, pos: Tuple[int, int], width: int, one_line: int, height: int, color: COLOR,
                 if_button: bool = False, color_disabled: COLOR = (30, 30, 30),
                 color_active: COLOR = (40, 40, 40), line=None) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.color = color
        self.surface.fill(self.color)
        self.if_button = if_button
        self.color_active = color_active
        self.color_disabled = color_disabled
        self.one_line = one_line
        self.line = line
        #
        self.lines = []

    def render(self, texts: list) -> None:
        self.lines = []
        height = self.one_line
        pos_text = Interface(pos=(self.rect.x, self.rect.y), max_width=self.rect.width, max_height=None,
                             size=(self.rect.width, height), indent=(0, height // 100))
        for text in texts:
            button = ChoiceButton(
                text=text, pos=pos_text.pos, width=pos_text.width, height=pos_text.height,
                color_active=self.color_active, color_disabled=self.color_disabled, line=self.line)
            self.lines.append(button)
            pos_text.move(0)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)
        for line in self.lines:
            line.draw(surface)

    def event(self, event: pg.event.Event) -> None:
        for line in self.lines:
            if type(line) in BUTTONS:
                line.event(event)
