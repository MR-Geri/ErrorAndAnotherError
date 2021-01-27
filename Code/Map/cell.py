from Code.settings import *
from Code.info_panel import RightPanel


class Cell:
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        super().__init__()
        self.number_x, self.number_y = number_x, number_y
        self.size_cell = size_cell
        self.panel = panel
        self.x = number_x * self.size_cell
        self.y = number_y * self.size_cell
        self.rect = pg.Rect(self.x, self.y, self.size_cell, self.size_cell)
        #
        self.render()

    def render(self) -> None:
        self.image = pg.Surface((self.size_cell, self.size_cell))
        self.image.fill(self.color)

    def info(self) -> None:
        self.panel.info_update = self.info
        self.panel.update_text(self.texts)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.x = self.number_x * size_cell
        self.y = self.number_y * size_cell
        self.rect = pg.Rect(self.x, self.y, self.size_cell, self.size_cell)
        self.render()

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)


class Plain(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#194D0F')
        self.name = ' Равнина '
        self.energy_passage = 10
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<База>']
        super().__init__(number_x, number_y, size_cell, panel)


class Swamp(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#32160D')
        self.name = ' Болото '
        self.energy_passage = 19
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<База>']
        super().__init__(number_x, number_y, size_cell, panel)


class Mountain(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#818394')
        self.name = ' Горы '
        self.energy_passage = 20
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<Шахта>']
        super().__init__(number_x, number_y, size_cell, panel)


class Desert(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#F0E500')
        self.name = ' Пустыня '
        self.energy_passage = 12
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<База>']
        super().__init__(number_x, number_y, size_cell, panel)


class IronOre(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#A46B4C')
        self.name = ' Железная руда '
        self.energy_passage = 20
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<Шахта>']
        self.ore = 'Железо'
        self.ore_quantity = 10
        super().__init__(number_x, number_y, size_cell, panel)


class GoldOre(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#DCCE33')
        self.name = ' Золотая руда '
        self.energy_passage = 20
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<Шахта>']
        self.ore = 'Золото'
        self.ore_quantity = 7
        super().__init__(number_x, number_y, size_cell, panel)


class CooperOre(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#DC8F15')
        self.name = ' Медная руда '
        self.energy_passage = 20
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<Шахта>']
        self.ore = 'Медь'
        self.ore_quantity = 20
        super().__init__(number_x, number_y, size_cell, panel)


class TinOre(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#EEEABA')
        self.name = ' Оловянная руда '
        self.energy_passage = 20
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<Шахта>']
        self.ore = 'Олово'
        self.ore_quantity = 15
        super().__init__(number_x, number_y, size_cell, panel)


class SiliconOre(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#2C3C34')
        self.name = ' Гравий '
        self.energy_passage = 20
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<Шахта>']
        self.ore = 'Кремний'
        self.ore_quantity = 30
        super().__init__(number_x, number_y, size_cell, panel)


class PlatinumOre(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel) -> None:
        self.color = pg.Color('#6BBEE0')
        self.name = ' Платиновая руда '
        self.energy_passage = 20
        self.texts = [self.name, f'Для перемещения', f'энергии > {self.energy_passage}', 'Можно разместить',
                      '<Шахта>']
        self.ore = 'Платина'
        self.ore_quantity = 5
        super().__init__(number_x, number_y, size_cell, panel)
