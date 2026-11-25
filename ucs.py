import math
import heapq
from itertools import count

# dude ucs fucking sucks !!!
def ucs(grid, start, goal, on_explore=None):
    # bounds of the grid
    max_row = len(grid)
    max_col = len(grid[0])

    # dx, dy, cost tuple
    moves = [(-1, 0, 1.0),  # left
             (1, 0, 1.0),   # right
             (0, -1, 1.0),  # up
             (0, 1, 1.0),   # down
             (-1, -1, math.sqrt(2)),  # up-left
             (1, -1, math.sqrt(2)),   # up-right
             (-1, 1, math.sqrt(2)),   # down-left
             (1, 1, math.sqrt(2))]    # down-right

    tie_breaker = count()

    # behold our priority queue: (cost, tie-breaker, node)
    frontier = [(0.0, next(tie_breaker), start)]
    visited = set()
    parent = {start: None}
    costs = {start: 0.0}
    explored = []

    while frontier:
        current_cost, _, curr_node = heapq.heappop(frontier)

        # if we got a cheaper path to this node, we skipping it
        if curr_node in visited:
            continue

        visited.add(curr_node)
        explored.append(curr_node)

        if on_explore is not None:
            on_explore(curr_node)

        if curr_node == goal:
            path = []
            curr = goal

            # so we just reconstruct the path from the goal back to the start
            while curr is not None:
                path.append(curr)
                curr = parent[curr]

            path.reverse()
            return path, current_cost, explored

        curr_x, curr_y = curr_node

        for move_x, move_y, move_cost in moves:
            new_x = curr_x + move_x
            new_y = curr_y + move_y

            if not (0 <= new_x < max_col and 0 <= new_y < max_row):
                continue

            # only nodes that are open can be entered
            if grid[new_y][new_x] != 0:
                continue

            # cant cut through walls diagonally woahhh
            if move_x != 0 and move_y != 0:
                if grid[curr_y][new_x] != 0 or grid[new_y][curr_x] != 0:
                    continue

            neighbor = (new_x, new_y)
            new_cost = current_cost + move_cost

            # add node if cheaper path found
            if neighbor not in visited and (neighbor not in costs or new_cost < costs[neighbor]):
                costs[neighbor] = new_cost
                parent[neighbor] = curr_node
                heapq.heappush(frontier, (new_cost, next(tie_breaker), neighbor))

    # no path found!! booooooooo
    return None, 0.0, explored
