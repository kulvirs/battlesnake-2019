from .grid import *

# Updates the board with food and returns a food list sorted by distance from head.
def add_food_to_board(food_data, head, board):
    foods = []
    for food in food_data:
        food_x, food_y = food['x'], food['y']
        if board.get_cell(food_x, food_y) in [EMPTY, FOOD]:
            board.update_grid_cell(food_x, food_y, FOOD)
        foods.append((food_x, food_y))

    return sorted(foods, key=lambda f: board.manhattan_distance(head[0], head[1], f[0], f[1]), reverse=True)

# Updates the board with location of snakes.
def add_snakes_to_board(snakes, id, length, board):
    for snake in snakes:
        snake_id = snake['id']
        snake_length = len(snake['body'])
        head = None
        for i, cell in enumerate(snake['body']):
            cell_x, cell_y = cell['x'], cell['y']
            if i == 0:
                    board.update_grid_cell(cell_x, cell_y, SNAKE_HEAD)
                    head = (cell_x, cell_y)
                    if snake_id != id:
                        if snake_length < length:
                            for x,y in board.get_neighbours_with_val(cell_x, cell_y, [EMPTY]):
                                board.update_grid_cell(x, y, TARGET)
                        else:
                            for x,y in board.get_neighbours_with_val(cell_x, cell_y, [EMPTY, TARGET, FOOD]):
                                board.update_grid_cell(x, y, DANGER)
                    else:
                        board.update_grid_cell(cell_x, cell_y, MY_HEAD)
            
            elif i != snake_length - 1 or len(board.get_neighbours_with_val(head[0], head[1], [FOOD])) > 0:
                board.update_grid_cell(cell_x, cell_y, OCCUPIED)
