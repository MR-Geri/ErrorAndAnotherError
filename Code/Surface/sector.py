import pygame as pg
from Code.settings import *
from Code.Surface.cell import Cell


class Sector:
    def __init__(self, width: int, height: int, size_cell: int) -> None:
        self.width, self.height = width, height  # Длина и высота сектора в единицах
        self.size_cell = size_cell
        self.size_sector = (width * size_cell, height * size_cell)
        self.surface = pg.Surface(self.size_sector)
        self.board = None
        # Инициализация
        self.gen_board()
        self.update()

    def gen_board(self) -> None:
        """
        Генерация поля (карты) в секторе.
        """
        self.board = [
            [Cell(number_x, number_y, self.size_cell) for number_x in range(self.width)]
            for number_y in range(self.height)
        ]

    def update(self) -> None:
        self.surface.fill(pg.Color(SECTORS_BACKGROUND_COLOR))
        for cells in self.board:
            for cell in cells:
                self.surface.blit(cell.image, cell.rect)

    def scale(self, size_cell):
        self.size_cell = size_cell
        self.size_sector = (self.width * size_cell, self.height * size_cell)
        self.surface = pg.Surface(self.size_sector)
        for cells in self.board:
            for cell in cells:
                cell.render(size_cell)
        self.update()
