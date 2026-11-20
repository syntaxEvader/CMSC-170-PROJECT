import math
from collections import deque
def bfs(grid, start, goal, on_explore=None):
    #bounds of the grid
    max_row=len(grid)
    max_col=len(grid[0])

    #x, y, cost tuple
    moves=[(-1,0,1.0), #left
           (1,0,1.0), #right
           (0,-1,1.0), #up
           (0, 1, 1.0), #down
           (-1,-1,math.sqrt(2)), #up-left
           (1,-1,math.sqrt(2)), #up-right
           (-1,1,math.sqrt(2)), #down-left
           (1,1,math.sqrt(2)) #down-right
    ]
    visited = [[False] * max_col for _ in range(max_row)]
    visited[start[1]][start[0]] = True #2d array for standard BFS, keeps track of visited nodes
    queue=deque([start]) #queue for standard BFS, keep track of ordering for nodes to visit
    parent={start: None} #for backtracking purposes later: format is {node:parent}
    costs={start: 0.0} #costs to get to each path
    explored=[] #list of nodes explored, keep track for statistics and animations

    valid_path=False #keeps track whether or not the path is found


    while queue and valid_path==False:
        #pop the current node and add it to visiited nodes
        curr_node=queue.popleft()

        explored.append(curr_node)
        if on_explore is not None:
            on_explore(curr_node)

        #if the current node is the goal node end the algo
        if curr_node==goal:
            valid_path=True
            break

        #iterate through all 8 possible directions, and go to the nodes that are possible to visit
        curr_x, curr_y=curr_node
        for move_x, move_y, move_cost in moves:
            new_x, new_y=(curr_x+move_x),(curr_y+move_y)
            #checks if the neighbor is within the bounds of the grid
            if 0<=new_x<max_col and 0<=new_y<max_row:
                #check if the value is open node or wall
                if grid[new_y][new_x]==0:
                    new_cost=costs[curr_node]+move_cost #cost to reach the neighbor
                    #update node as visited if not already visited
                    if move_x != 0 and move_y != 0:
                        if grid[curr_y][new_x] != 0 or grid[new_y][curr_x] != 0:
                            continue
                    if not visited[new_y][new_x]:
                        visited[new_y][new_x] = True #change 2d array value to true
                        parent[(new_x,new_y)]=curr_node #add parent data
                        costs[(new_x,new_y)]=new_cost #add cost
                        queue.append((new_x,new_y)) #append to the quqeue
    #if no path was found stop but return the nodes explored for visualization and eval
    if valid_path==False:
        return None, 0.0, explored

    path=[]
    curr=goal
    #reverses the traversed path
    while curr is not None:
        path.append(curr)
        curr=parent[curr]
    path.reverse()
    path_cost=costs[goal]
    return path, path_cost, explored