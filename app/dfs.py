from .grid import *

def find_component(source, head, board):
    dist = board.manhattan_distance(head[0], head[1], source[0], source[1])
    stack = [source]

    visited = {}
    size = 0
    closer_heads = []
    reachable = False

    while stack:
        v = stack.pop()
        if not visited.get(v, False):
            if v == head:
                reachable = True
            else:
                size += 1
                val = board.get_cell(v[0], v[1])

                if val == SNAKE_HEAD and board.manhattan_distance(v[0], v[1], source[0], source[1]) < dist:
                    closer_heads.append(v)

                visited[v] = True
                for neighbour in board.get_neighbours_with_val(v[0], v[1], [EMPTY, FOOD, DANGER, TARGET, MY_HEAD]):
                    stack.append(neighbour)

    return size, reachable, closer_heads

def choose_largest_component(head, board, length):
    moves = []
    for neighbour in board.get_neighbours_with_val(head[0], head[1], [EMPTY, FOOD, TARGET, DANGER]):
        size, _, _ = find_component(neighbour, head, board)
        if size <= length:
            moves.append([neighbour, size])

    danger_move, danger_size = None, 0
    safe_move, safe_size = None, 0
    for move, size in moves:
        val = board.get_cell(move[0], move[1])
        if val == DANGER and size > danger_size:
            danger_move, danger_size = move, size
        elif val != DANGER and size > safe_size:
            safe_move, safe_size = move, size

    if safe_move:
        return board.get_direction(head[0], head[1], safe_move[0], safe_move[1])
    elif danger_move:
        return board.get_direction(head[0], head[1], danger_move[0], danger_move[1])
    else:
        return None
