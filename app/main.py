import json
import os
import random
import bottle
import sys

from .api import ping_response, start_response, move_response, end_response
from .grid import Grid, EMPTY, OCCUPIED, FOOD
from .random_snake import get_valid_random_move

board = Grid()

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
    board.create_grid(data['board']['height'], data['board']['width'])
    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    sys.stdout.flush()
    data = bottle.request.json
    board.clear()

    head = [data['you']['body'][0]['x'], data['you']['body'][0]['y']]
    health = data['you']['health']
    id = data['you']['id']

    for food in data['board']['food']:
        board.update_grid_cell(food['x'], food['y'], FOOD)

    for snake in data['board']['snakes']:
        for cell in snake['body']:
            board.update_grid_cell(cell['x'], cell['y'], OCCUPIED)
            
    move = get_valid_random_move(board, head)
    return move_response(move if move else random.choice(['up', 'down', 'left', 'right']))


@bottle.post('/end')
def end():
    data = bottle.request.json
    board.clear()

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
