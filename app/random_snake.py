import random

from .grid import Grid, EMPTY, OCCUPIED, FOOD

def get_valid_random_move(board, head):
    moves = board.get_neighbours_with_val(head[0], head[1], [FOOD, EMPTY])
    if moves:
        move = random.choice(moves)
        return board.get_direction(head[0], head[1], move[0], move[1])
    return None  