from math import inf, sqrt
import heapq

_DIAGONAL_COST = sqrt(2)
# a move is a (x, y, cost) tuple
_MOVES = (
    (-1, 0, 1.0), # left
    (1, 0, 1.0), # right
    (0, -1, 1.0), # up
    (0, 1, 1.0), # down
    (-1, -1, _DIAGONAL_COST), # up-left
    (1, -1, _DIAGONAL_COST), # up-right
    (-1, 1, _DIAGONAL_COST), # down-left
    (1, 1, _DIAGONAL_COST), # down-right
)

# octile distance is the heuristic to be used in this A* algorithm
def octile_distance(start, goal):
    # to calculate the octile distance between two points in a grid, we can use the following formula:
    dx = abs(start[0] - goal[0])
    dy = abs(start[1] - goal[1])

    return max(dx,dy) + min(dx,dy) * (_DIAGONAL_COST-1)

def isOpen(grid, x, y):
    if x < 0 or x >= len(grid[0]):
        return False
    if y < 0 or y >= len(grid):
        return False
    if grid[y][x] == 0:
        return True
    else:
        return False

def getF(cell, gValue, goal):
    return gValue[cell] + octile_distance(cell, goal)
def removeMinF(openList, gValue): 
    while openList:
        _, negativeQueuedCost, x, y = heapq.heappop(openList)
        cell = (x, y)

        # Ignore an older entry if this cell has since gotten a cheaper route.
        queuedCost = -negativeQueuedCost
        if queuedCost == gValue.get(cell):
            return cell
    return None

def goalTest(cell, goal):
    if cell == goal:
        return True
    else:
        return False

def a_star(grid, start, goal, on_explore=None, *, collect_explored=True):
    if not grid or not grid[0]:
        raise ValueError("Grid must contain at least one cell")
    if any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("Grid rows must all have the same width")
    height, width = len(grid), len(grid[0])
    openList = [(octile_distance(start, goal), -0.0, start[0], start[1])] # use a min heap for faster accessing
    gValue = {start: 0.0} # g value is the cost from start to node
    parentDict = {} # node: parent value pairs
    goalPath = []  # stores the shortest path
    explored = [] if collect_explored else None # stores the explored cells

    if start == goal:
        return [start], 0, explored or []

    # validate start and goal first 
    if not isOpen(grid, start[0], start[1]):
        return None, None, []
    if not isOpen(grid, goal[0], goal[1]):
        return None, None, []

    # main a* loop
    while(openList != []):
        bestNode = removeMinF(openList, gValue)
        if bestNode is None:
            break
        x, y = bestNode

        if goalTest(bestNode, goal):
            #get path from start to goal node
            parent = bestNode
            while parent != start:
                goalPath.append(parent)
                parent = parentDict[parent]
            goalPath.append(start)
            goalPath.reverse()

            return goalPath, gValue[bestNode], explored or []
        
        # for visualization
        if explored is not None:
            explored.append(bestNode)
        if on_explore is not None:
            on_explore(bestNode)

        # get possible neighbors, check if they are walkable
        for dx, dy, move_cost in _MOVES:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= width or ny < 0 or ny >= height or grid[ny][nx] != 0:
                continue

            if dx != 0 and dy != 0:
                if grid[y][nx] != 0 or grid[ny][x] != 0:
                    continue
            neighbor = (nx, ny)
            # update cost if it is less than the current cost
            newCost = gValue[bestNode] + move_cost
            if newCost < gValue.get(neighbor, inf):
                parentDict[neighbor] = bestNode
                gValue[neighbor] = newCost
                # add neighbor to open list
                priority = newCost + octile_distance(neighbor, goal)
                heapq.heappush(openList, (priority, -newCost, neighbor[0], neighbor[1]))

    return None, None, []