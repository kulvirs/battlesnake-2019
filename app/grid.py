EMPTY = 0
OCCUPIED = 1
FOOD = 2
DANGER = 3
SNAKE_HEAD = 4
TARGET = 5
MY_HEAD = 6

class Grid:

    # Initializes a two-dimensional array representing the grid.
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = [[EMPTY for i in range(self.width)] for j in range(self.height)]

    # Returns true if the given coordinates exist on the board, false otherwise.
    def valid_coordinates(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    # Gets the manhattan distance between two cells on the grid.
    def manhattan_distance(self, x1, y1, x2, y2):
        return abs(y2-y1) + abs(x2-x1)

    # Updates the value at a specific grid cell.
    def update_grid_cell(self, x, y, val):
        if self.valid_coordinates(x, y):
            self.grid[y][x] = val

    def get_cell(self, x, y):
        return self.grid[y][x]

    # Returns the coordinates of all neighbours of the given cell.
    def get_neighbours(self, x, y):
        neighbours = []

        if self.valid_coordinates(x, y):
            if x > 0:
                neighbours.append((x-1, y))
            if x < self.width-1:
                neighbours.append((x+1, y))
            if y > 0:
                neighbours.append((x, y-1))
            if y < self.height-1:
                neighbours.append((x, y+1)) 

        return neighbours

    # Returns the coordinates of all neighbours of the given cell that have a value that exists in the given values list.
    def get_neighbours_with_val(self, x, y, vals):
        neighbours = self.get_neighbours(x, y)
        return [(x,y) for x,y in neighbours if self.grid[y][x] in vals]

    # Returns the direction (up, down, left, right) to move to get from (x1, y1) to (x2, y2)
    def get_direction(self, x1, y1, x2, y2):
        if self.valid_coordinates(x1, y1) and self.valid_coordinates(x2, y2):
            if x2 != x1:
                return "right" if x2 > x1 else "left"
            elif y2 != y1:
                return "down" if y2 > y1 else "up"
            
