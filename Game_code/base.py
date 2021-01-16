from typing import Tuple, Union


# Логика базы для зарядки робота
def energy_transfer(state, board, entities) -> Union[Tuple[int, Tuple[int, int]], None]:
    robot = entities[28][0]
    if robot:
        if robot['energy'] < robot['energy_max']:
            robot['permissions'].set_move(False)
            return 5, (0, 28)
        else:
            robot['permissions'].set_move(True)
    return None
