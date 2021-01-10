class RadioisotopeGenerator:
    def __init__(self, increase_energy) -> None:
        self.increase_energy = increase_energy
        self.energy_generate = 1
        self.energy_tick = 8
        self.resource = 10 ** 6

    def update(self, tick: int) -> None:
        if not tick % self.energy_tick and self.resource:
            self.resource -= self.energy_generate
            self.increase_energy(self.energy_generate)
