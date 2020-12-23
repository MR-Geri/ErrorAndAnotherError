import random
from typing import Tuple

from Code.settings import *


class Biome:
    def __init__(self, number_x: int, number_y: int, size_cell: int, cell: ALL_CELL) -> None:
        self.number_x = number_x
        self.number_y = number_y
        self.cell = cell
        self.size_cell = size_cell
        #
        self.all_cell = self.gen_all_cell()

    def gen_all_cell(self) -> list:
        all_cell = []
        # Пока не ткнём в пустое место
        # number_xy = (random.randint(0, self.number_x), random.randint(0, self.number_y))
        # size = random.randint(0, self.number_xy[0] * self.number_xy[1])
        # pos = (random.randint(0, size_sector[0]), random.randint(0, size_sector[1]))
        for i in range(self.size):
            pass
        return all_cell


class BiomeMountain(Biome):
    def __init__(self, number_x: int, number_y: int, size_cell: int) -> None:
        super().__init__(number_x=number_x, number_y=number_y, size_cell=size_cell, cell=Mountain)


class GeneratorBiomes:
    def __init__(self, number_x: int, number_y: int, size_cell: int):
        self.number_x = number_x
        self.number_y = number_y
        self.size_cell = size_cell
        #
        self.mountain = [BiomeMountain(self.number_x, self.number_y, self.size_cell)]  # Несколько биомов гор random!
        #
        self.biomes = self.mountain + []

    def check(self, x: int, y: int) -> bool:

        return False

    def get_cell(self, x: int, y: int) -> ALL_CELL:
        return
