import pygame as pg


class Cell(pg.sprite.Sprite):
    def __init__(self, number_x: int, number_y: int, size_cell: int) -> None:
        super().__init__()
        self.number_x, self.number_y = number_x, number_y
        self.size_cell = size_cell
        self.x = number_x * self.size_cell
        self.y = number_y * self.size_cell
        self.rect = pg.Rect(self.x, self.y, self.size_cell, self.size_cell)
        #
        self.render()

    def render(self) -> None:
        self.image = pg.Surface((self.size_cell, self.size_cell))
        self.image.fill(self.color)
        #
        # pg.draw.rect(
        #     self.image,
        #     pg.Color((255, 255, 255)),
        #     (0.25 * self.size_cell, 0.25 * self.size_cell, 0.5 * self.size_cell, 0.5 * self.size_cell)
        # )

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.x = self.number_x * size_cell
        self.y = self.number_y * size_cell
        self.rect = pg.Rect(self.x, self.y, self.size_cell, self.size_cell)
        self.render()

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)


class Plain(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int) -> None:
        self.color = pg.Color('#194D0F')
        super().__init__(number_x, number_y, size_cell)


class Swamp(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int) -> None:
        self.color = pg.Color('#32160D')
        super().__init__(number_x, number_y, size_cell)


class Mountain(Cell):
    def __init__(self, number_x: int, number_y: int, size_cell: int) -> None:
        self.color = pg.Color('#818394')
        super().__init__(number_x, number_y, size_cell)
