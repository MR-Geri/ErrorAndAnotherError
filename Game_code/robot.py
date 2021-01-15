from typing import Tuple, Union


def move(state, board, entities) -> Union[Tuple[int, int], None]:
    pos = state['pos']
    return pos[0] + 1, pos[1]