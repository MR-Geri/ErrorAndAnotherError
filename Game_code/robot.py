from typing import Tuple, Union


def move(state, board, entities) -> Union[Tuple[int, int], None]:
    pos = state['pos']
    if state['energy'] <= state['energy_max'] // 2 or \
            sum([sum(i.values()) for i in state['inventory'].values()]) == state['inventory_max']:
        return pos[0] - 1, pos[1]
    return pos[0] + 1, pos[1]


def mine(state, board, entities) -> Union[Tuple[int, int], None]:
    pos = state['pos']
    if sum([sum(i.values()) for i in state['inventory'].values()]) < state['inventory_max'] and \
            board[pos[1]][pos[0] + 1]['name'] in ['IronOre']:
        state['permissions'].can_move = False
        return pos[0] + 1, pos[1]
    state['permissions'].can_move = True
    return None


def transfer():
    return None
