from .grid import *

# Returns true if snake should be passive.
def passive_heuristic(board, health, head, food, board_dim, length, id, num_snakes, snakes):
    if num_snakes <= 2:
        for snake in snakes:
            if snake['id'] != id:
                return len(snake['body']) + 2 < length and health - board.manhattan_distance(head[0], head[1], food[0], food[1]) > 2*board_dim
        return False
        #return health - board.manhattan_distance(head[0], head[1], food[0], food[1]) > 8*board_dim + 1 and length > 4
    return health - board.manhattan_distance(head[0], head[1], food[0], food[1]) > 6*board_dim + 1 and length > 4