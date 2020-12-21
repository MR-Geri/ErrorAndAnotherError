import random
from typing import Tuple
import pygame as pg

from Code.settings import *
from Code.Surface.cell import Plain, Swamp, Mountain


class Biome:
    def __init__(self, max_size_x: int, max_size_y: int, size_sector: Tuple[int, int]) -> None:
        self.max_size = (random.randint(0, max_size_x), random.randint(0, max_size_y))
        self.size = random.randint(0, self.max_size[0] * self.max_size[1])
        self.pos = (random.randint(0, size_sector[0]), random.randint(0, size_sector[1]))
        self.all_pos = self.gen_all_pos()

    def gen_all_pos(self) -> list:
        print(self.size)
        return list()


class GeneratorBiomes:
    def __init__(self, max_size_x: int, max_size_y: int, size_sector: Tuple[int, int]):
        self.all_pos = []
        self.mountain = Biome(max_size_x, max_size_y, size_sector)

    def check(self, x: int, y: int) -> bool:
        return False

    def get_biomes(self, x: int, y: int):
        return None


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
        Генерация сектора.
        """
        biomes = GeneratorBiomes(self.size_sector[0] // 10, self.size_sector[1] // 10, self.size_sector)
        print(biomes.mountain.max_size, biomes.mountain.pos)
        self.board = [
            [
                Mountain(number_x, number_y, self.size_cell)
                if biomes.check(number_x, number_y) else
                Plain(number_x, number_y, self.size_cell)
                for number_x in range(self.width)]
            for number_y in range(self.height)
        ]

    def update(self) -> None:
        self.surface.fill(pg.Color(BACKGROUND_COLOR))
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
