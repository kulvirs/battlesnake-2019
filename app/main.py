import json
import os
import random
import bottle
import sys

from .api import *
from .random_snake import *
from .path_finder_snake import *
from .utils import *
from .dfs import *
from .passive import *

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json
    color = "#8A2BE2"

    return start_response(color)


@bottle.post('/move')
def move():
    sys.stdout.flush()
    data = bottle.request.json

    head = (data['you']['body'][0]['x'], data['you']['body'][0]['y']) 
    health = data['you']['health']
    id = data['you']['id']
    length = len(data['you']['body'])
    tail = (data['you']['body'][length-1]['x'], data['you']['body'][length-1]['y'])
    height = data['board']['height']
    width = data['board']['width']
    num_snakes = len(data['board']['snakes'])

    board = Grid(height, width)

    add_snakes_to_board(data['board']['snakes'], id, length, board)
    foods = add_food_to_board(data['board']['food'], head, board)

    largest_reachable_food, largest_size = None, 0
    safest_food = None
    move = None

    while foods:
        candidate_food = foods.pop()
        component_size, reachable, heads = find_component(candidate_food, head, board)
        if component_size < length or not reachable or heads:
            if component_size > largest_size and reachable:
                largest_reachable_food, largest_size = candidate_food, component_size
        else:
            print("found safest food")
            safest_food = candidate_food
            break
    
    target_food = safest_food if safest_food else largest_reachable_food

    if target_food and not passive_heuristic(board, health, head, target_food, height, length, id, num_snakes, data['board']['snakes']):
        # Need food.
        print("looking for food", target_food)
        move = a_star_search(head, target_food, board)

    if not move:
        # Look for targets
        print("looking for targets")
        targets = board.get_neighbours_with_val(head[0], head[1], [TARGET])
        for target in targets:
            size, reachable, _ = find_component(target, head, board)
            if size > length and reachable:
                move = board.get_direction(head[0], head[1], target[0], target[1])
                break
        
    if not move:
        # Chase tail
        print("chasing tail")
        move = a_star_search(head, tail, board)

    if not move:
        # Choose largest component.
        print("choosing largest component")
        move = choose_largest_component(head, board, length)     

    if not move:
        # Choose valid random move
        print("choosing random valid move")
        move = get_valid_random_move(board, head)

    if not move:
        print("no valid moves")
        move = random.choice(['up', 'down', 'left', 'right'])

    return move_response(move)


@bottle.post('/end')
def end():
    data = bottle.request.json
    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    port = '8080' if len(sys.argv) <= 1 else sys.argv[1]
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', port),
        debug=os.getenv('DEBUG', True)
    )
