from Code.settings import *
from Code.texts import max_size_list_text
from Code.utils import Interface


class Inventory:
    def __init__(self) -> None:
        self.rect = None
        self.surface = None
        self.resources = {
            'Железо': {'обработано': 0, 'сырьё': 0},
            'Сталь': {'обработано': 0, 'сырьё': 0},
            'Золото': {'обработано': 0, 'сырьё': 0},
            'Медь': {'обработано': 0, 'сырьё': 0},
            'Олово': {'обработано': 0, 'сырьё': 0},
            'Кремний': {'обработано': 0, 'сырьё': 0},
            'Платина': {'обработано': 0, 'сырьё': 0},
        }

    def init(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((width, height))
        self.render()

    def save(self) -> None:
        pass

    def load(self) -> None:
        pass

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def update(self, resource: str, condition: bool = False, quantity: int = 0) -> None:
        condition = 'обработано' if condition else 'сырьё'
        self.resources[resource][condition] += quantity
        self.render()

    def render(self) -> None:
        self.surface.fill(COLOR_BACKGROUND)
        w80, w10 = int(self.rect.width * 0.5), int(self.rect.width * 0.25)
        interface = Interface((0, 0), max_width=self.rect.width, max_height=self.rect.height,
                              indent=(0, self.rect.height // 54), size=(self.rect.width, self.rect.height // 9))
        size = max_size_list_text(['Продукт', 'Сырьё'], w10, interface.height, font_type=PT_MONO)
        text = TextMaxSizeCenter(text=f'Ресурс', pos=interface.pos, width=w80, height=interface.height,
                                 font_type=PT_MONO)
        text.draw(self.surface)
        text = TextCenter(text=f'Продукт', pos=(interface.pos[0] + w80, interface.pos[1]),
                          width=w10, height=interface.height, font_size=size, font_type=PT_MONO)
        text.draw(self.surface)
        text = TextCenter(text=f'Сырьё', pos=(interface.pos[0] + w80 + w10, interface.pos[1]),
                          width=w10, height=interface.height, font_size=size, font_type=PT_MONO)
        text.draw(self.surface)
        interface.move(0)
        for element in self.resources.keys():
            text = TextMaxSizeCenter(text=element, pos=interface.pos, width=w80, height=interface.height,
                                     font_type=PT_MONO)
            text.draw(self.surface)
            text = TextMaxSizeCenter(text=str(self.resources[element]['обработано']),
                                     pos=(interface.pos[0] + w80, interface.pos[1]),
                                     width=w10, height=interface.height, font_type=PT_MONO)
            text.draw(self.surface)
            text = TextMaxSizeCenter(text=str(self.resources[element]['сырьё']),
                                     pos=(interface.pos[0] + w80 + w10, interface.pos[1]),
                                     width=w10, height=interface.height, font_type=PT_MONO)
            text.draw(self.surface)
            interface.move(0)
