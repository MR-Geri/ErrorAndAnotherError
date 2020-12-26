from typing import Tuple
import pygame as pg

from Code.Map.biomes import GeneratorBiomes
from Code.settings import *


class Sector:
    def __init__(self, number_x: int, number_y: int, size_cell: int) -> None:
        self.number_x, self.number_y = number_x, number_y  # Длина и высота сектора в единицах
        self.size_cell = size_cell
        self.size_sector = (number_x * size_cell, number_y * size_cell)
        self.surface = pg.Surface(self.size_sector)
        self.board = None
        # Инициализация
        self.gen_board()
        self.update()

    def gen_board(self) -> None:
        """
        Генерация сектора.
        """
        biomes = GeneratorBiomes(
            number_x=self.number_x,
            number_y=self.number_y,
            size_cell=self.size_cell
        )
        self.board = [
            [biomes.get_cell(x, y) for x in range(self.number_x)]
            for y in range(self.number_y)
        ]

    def update(self) -> None:
        self.surface.fill(pg.Color(BACKGROUND_COLOR))
        for cells in self.board:
            for cell in cells:
                self.surface.blit(cell.image, cell.rect)

    def scale(self, size_cell):
        self.size_cell = size_cell
        self.size_sector = (self.number_x * size_cell, self.number_y * size_cell)
        self.surface = pg.Surface(self.size_sector)
        for cells in self.board:
            for cell in cells:
                cell.render(size_cell)
        self.update()