from math import inf, sqrt

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
def removeMinF(openList, gValue, goal): 
    currmin = inf
    minIndex = 0

    for i in range(len(openList)):
        currentF = getF(openList[i], gValue, goal)
        if  currentF < currmin:
            currmin = currentF
            minIndex = i    

    return openList.pop(minIndex)
def goalTest(cell, goal):
    if cell == goal:
        return True
    else:
        return False

def a_star(grid, start, goal, on_explore=None):
    if not grid or not grid[0]:
        raise ValueError("Grid must contain at least one cell")
    if any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("Grid rows must all have the same width")
    height, width = len(grid), len(grid[0])
    inOpen = [[False] * width for _ in range(height)]
    openList = [start]
    gValue = {start: 0.0} # g value is the cost from start to node
    parentDict = {} # node: parent value pairs
    goalPath = []  # stores the shortest path
    explored = []  # stores the explored cells

    if start == goal:
        return [start], 0, []

    # validate start and goal first 
    if not isOpen(grid, start[0], start[1]):
        return None, None, []
    if not isOpen(grid, goal[0], goal[1]):
        return None, None, []

    # main a* loop
    while(openList != []):
        bestNode = removeMinF(openList, gValue, goal)
        x, y = bestNode
        inOpen[y][x] = False

        if goalTest(bestNode, goal):
            #get path from start to goal node
            parent = bestNode
            while parent != start:
                goalPath.append(parent)
                parent = parentDict[parent]
            goalPath.append(start)
            goalPath.reverse()

            return goalPath, gValue[bestNode], explored
        
        # for visualization
        explored.append(bestNode)
        if on_explore is not None:
            on_explore(bestNode)

        # get possible neighbors, check if they are walkable
        for i in _MOVES:
            neighbor = (x+i[0], y+i[1])

            if not isOpen(grid, neighbor[0], neighbor[1]):
                continue

            if i[0] != 0 and i[1] != 0:
                if grid[y][x + i[0]] == 1 or grid[y + i[1]][x] == 1:
                    continue
            # update cost if it is less than the current cost
            newCost = gValue[bestNode] + i[2]
            if newCost < gValue.get(neighbor, inf):
                parentDict[neighbor] = bestNode
                gValue[neighbor] = newCost
                # add neighbor to open list
                if not inOpen[neighbor[1]][neighbor[0]]:
                    openList.append(neighbor)
                    inOpen[neighbor[1]][neighbor[0]] = True

    return None, None, []