from .grid import *

# Returns true if snake should be passive.
def passive_heuristic(board, health, head, food, board_dim, length):
    return health - board.manhattan_distance(head[0], head[1], food[0], food[1]) > 2*board_dim + 1 and length > 4