from Code.info_panel import RightPanel
from Code.settings import *

import random
from collections import defaultdict
from typing import Tuple


class Biome:
    def __init__(self, number_x: int, number_y: int, max_size_biome: Tuple[int, int], min_quantity: int,
                 size_cell: int, cell: ALL_CELL, panel: RightPanel) -> None:
        self.number_x = number_x
        self.number_y = number_y
        self.max_size_biome = max_size_biome
        self.cell = cell
        self.size_cell = size_cell
        self.panel = panel
        #
        self.number_xy = (random.randint(1, self.max_size_biome[0]), random.randint(1, self.max_size_biome[1]))
        self.size = random.randint(min_quantity, self.max_size_biome[0] * self.max_size_biome[1])
        self.pos = (
            random.randint(self.number_xy[0], self.number_x - self.number_xy[0]),
            random.randint(self.number_xy[1], self.number_y - self.number_xy[1])
        )
        #
        self.cells, self.cords_cells = self.gen_all_cell()

    def new_possible(self, possible: list, pos: Tuple[int, int]) -> list:
        x, y = pos
        possible.remove(pos)
        for _x, _y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if 0 <= _x <= self.number_xy[0] + self.pos[0] and 0 <= _y <= self.number_xy[1] + self.pos[1]:
                possible.append((_x, _y))
        return possible

    def gen_all_cell(self) -> Tuple[defaultdict, set]:
        cells, cords_cells = defaultdict(lambda: defaultdict()), set()
        pos_0 = self.pos[0] + self.number_xy[0] // 2, self.pos[1] + self.number_xy[1] // 2
        possible = self.new_possible([pos_0], pos_0)
        for i in range(self.size):
            pos = random.choice(possible)
            possible = self.new_possible(possible, pos)
            cells[pos[1]][pos[0]] = self.cell(*pos, self.size_cell, self.panel)
            cords_cells.add(pos)
        return cells, cords_cells


class BiomeMountain(Biome):
    def __init__(self, number_x: int, number_y: int, max_size_biome: Tuple[int, int],
                 min_quantity: int, size_cell: int, panel: RightPanel) -> None:
        super().__init__(number_x=number_x, number_y=number_y, max_size_biome=max_size_biome,
                         min_quantity=min_quantity, size_cell=size_cell, cell=Mountain, panel=panel)


class BiomeSwamp(Biome):
    def __init__(self, number_x: int, number_y: int, max_size_biome: Tuple[int, int],
                 min_quantity: int, size_cell: int, panel: RightPanel) -> None:
        super().__init__(number_x=number_x, number_y=number_y, max_size_biome=max_size_biome,
                         min_quantity=min_quantity, size_cell=size_cell, cell=Swamp, panel=panel)


class GeneratorBiomes:
    def __init__(self, number_x: int, number_y: int, size_cell: int, panel: RightPanel):
        self.number_x = number_x
        self.number_y = number_y
        self.size_cell = size_cell
        self.panel = panel
        #
        self.mountain = []
        self.swamp = []
        self.for_biomes = [
            (BiomeMountain, MAX_QUANTITY_MOUNTAIN, MIN_QUANTITY_MOUNTAIN_CELL, MAX_SIZE_MOUNTAIN, self.mountain),
            (BiomeSwamp, MAX_QUANTITY_SWAMP, MIN_QUANTITY_SWAMP_CELL, MAX_SIZE_SWAMP, self.swamp)
        ]
        #
        self.biomes = []
        self.gen_biomes()

    def get_cell(self, x: int, y: int) -> ALL_CELL:
        # Можно переделать на ХЕШ таблицы (словари)
        for group in self.biomes:
            for biome_ in group:
                if (x, y) in biome_.cords_cells:
                    return biome_.cells[y][x]
        return Plain(x, y, self.size_cell, self.panel)

    def entering_biome(self, biome) -> bool:
        # Можно переделать на ХЕШ таблицы (словари)
        for group in self.biomes:
            for biome_ in group:
                if biome.cords_cells.intersection(biome_.cords_cells):
                    return False
        return True

    def gen_biomes(self) -> None:
        for biome, quantity, min_quantity, max_size_biome, link_biome in self.for_biomes:
            for i in range(quantity):
                while True:
                    temp_biome = biome(self.number_x, self.number_y, max_size_biome, min_quantity, self.size_cell,
                                       self.panel)
                    if self.entering_biome(temp_biome):
                        break
                link_biome.append(temp_biome)
            self.biomes.append(link_biome)
