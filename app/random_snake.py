import random

from .grid import *

def get_valid_random_move(board, head):
    moves = board.get_neighbours_with_val(head[0], head[1], [TARGET, FOOD, EMPTY, DANGER])
    
    targets = []
    empty = []
    danger = []

    for move in moves:
        val = board.get_cell(move[0], move[1])
        if val == TARGET:
            targets.append(move)
        elif val == EMPTY or val == FOOD:
            empty.append(move)
        else:
            danger.append(move)
    
    move = None
    if targets:
        move = random.choice(targets)
    elif empty:
        move = random.choice(empty)
    elif danger:
        move = random.choice(danger)

    if move:
        return board.get_direction(head[0], head[1], move[0], move[1])

    return None  