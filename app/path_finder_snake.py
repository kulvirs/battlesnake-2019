from heapq import heappush, heappop

from .grid import *

# Takes in two tuples of the x and y coordinates and finds a path from source to destination.
def a_star_search(source, dest, board):
    pq = []
    heappush(pq, (0, source))

    visited = {source: False}
    prev = {source: None}
    dist = {}

    while pq:
        dist_u, u = heappop(pq)

        if not visited.get(u, False):
            visited[u] = True

            if u == dest:
                while prev.get(u, -1) != source:
                    u = prev.get(u, -1)
                    if u == -1:
                        return None
                return board.get_direction(source[0], source[1], u[0], u[1])
            
            if u == source:
                valid_types = [EMPTY, FOOD, TARGET]
            else:
                valid_types = [EMPTY, FOOD, TARGET, DANGER]

            for neighbour in board.get_neighbours_with_val(u[0], u[1], valid_types):
                alt = dist_u + 1 + board.manhattan_distance(neighbour[0], neighbour[1], dest[0], dest[1])
                
                if alt < dist.get(neighbour, float('inf')):
                    dist[neighbour] = alt
                    prev[neighbour] = u
                    heappush(pq, (dist[neighbour], neighbour))

    return None