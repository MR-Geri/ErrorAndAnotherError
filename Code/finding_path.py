import heapq
from numba import njit
from Code.settings import SECTOR_Y_NUMBER, SECTOR_X_NUMBER


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


@njit(cache=True)
def check(x, y, board):
    return True if 0 <= x < SECTOR_X_NUMBER and 0 <= y < SECTOR_Y_NUMBER and board[y, x] != 1 else False


@njit(cache=True, fastmath=True)
def get_next_nodes(x, y, board, distance) -> list:
    ways = [(x, y) for x in range(-distance, distance + 1) for y in range(-distance, distance + 1)]
    return [(x + dx, y + dy) for dx, dy in ways if check(x + dx, y + dy, board)]


@njit(cache=True)
def heuristic(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(x1, y1, x2, y2, board, distance):
    frontier = PriorityQueue()
    frontier.put((x1, y1), 0)
    came_from = {(x1, y1): None}

    while not frontier.empty():
        current = frontier.get()

        if current == (x2, y2):
            break

        for next in get_next_nodes(*current, board, distance):
            if next not in came_from:
                priority = heuristic(x2, y2, *next)
                frontier.put(next, priority)
                came_from[next] = current

    return (x2, y2) in came_from, came_from
