from typing import Union


def energy_transfer(state, board, entities) -> Union[list, None]:
    robots = []
    pos = state['pos']
    for y in range(pos[1] - state['distance_charging'], pos[1] + state['distance_charging'] + 1):
        for x in range(pos[0] - state['distance_charging'], pos[0] + state['distance_charging'] + 1):
            if state['pos'] != (x, y) and state['permissions'].can_charging and state['energy'] > 200:
                robot = entities[y][x]
                if robot:
                    if robot['energy'] < robot['energy_max']:
                        robot['permissions'].set_move(False)
                        robots.append((5, (x, y)))
                    else:
                        robot['permissions'].set_move(True)
    return robots if robots else None


def item_transfer(state, board, entities):
    pos = state['pos']
    for y in range(pos[1] - state['distance_resource'], pos[1] + state['distance_resource'] + 1):
        for x in range(pos[0] - state['distance_resource'], pos[0] + state['distance_resource'] + 1):
            if state['pos'] != (x, y) and state['permissions'].can_item_transfer:
                robot = entities[y][x]
                if robot:
                    invent = state['inventory']
                    for element in invent:
                        for i in invent[element]:
                            if invent[element][i] > 0 and sum([sum(i.values()) for i in robot['inventory'].values()]) \
                                    < robot['inventory_max']:
                                return robot['pos'], element, i, 10
    return None
