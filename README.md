# snekans

Meet snekans, the snake AI created by me and @Mailey1 for the Battlesnake 2019 programming competition. The main template for this snake was adapted from the sample snake code at https://github.com/battlesnakeio/starter-snake-python. Snekans is deployed on Heroku at https://snekans.herokuapp.com/ (currently offline for maintenance).

The snake uses an A* search algorithm to find the shortest path to available food. The Euclidean distance between each grid cell and the desired food is used as the heuristic to minimize the number of cells the algorithm searches through to find an optimal path. 

In order to avoid getting trapped by other snakes or within its own body, snekans also uses breadth-first search to find the connected components it is adjacent to. This ensures it does not enter a component of the grid that is too small for it. 

Extra game logic was also added to keep snekans from being too greedy and always eating food. Snekans only eats if it's health is below a certain threshold that is determined relative to the distance of the closest food or if it is not the largest snake on the board. 
