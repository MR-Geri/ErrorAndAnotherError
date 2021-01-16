from typing import Union


# Логика базы для зарядки робота
def energy_transfer(state, board, entities) -> Union[list, None]:
    robots = []
    pos = state['pos']
    for y in range(pos[1] - state['distance_charging'], pos[1] + state['distance_charging'] + 1):
        for x in range(pos[0] - state['distance_charging'], pos[0] + state['distance_charging'] + 1):
            if state['pos'] != (x, y) and state['permissions'].can_charging:
                robot = entities[y][x]
                if robot:
                    if robot['energy'] < robot['energy_max']:
                        robot['permissions'].set_move(False)
                        robots.append((5, (x, y)))
                    else:
                        robot['permissions'].set_move(True)
    return robots if robots else None
