import math

#ref:https://www.geeksforgeeks.org/dsa/greedy-best-first-search-algorithm/

#octile distance is the heuristic to be used in this GBFS algorithm
def octile_distance(start, goal):
    # to calculate the octile distance between two points in a grid, we can use the following formula:
    dx = abs(start[0] - goal[0])
    dy = abs(start[1] - goal[1])
    return max(dx,dy) + min(dx,dy) * (math.sqrt(2)-1)

def greedy(grid, start, goal, on_explore=None):
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

    nodes=[start]
    parent={start: None}
    costs={start: 0.0}
    explored=[]

    valid_path=False
    while nodes:
        best_node=0
        best_h=octile_distance(nodes[best_node], goal)

        for i in range(1,len(nodes)): #skip the first node since that is the curr best node
            h=octile_distance(nodes[i],goal) 
            if h<best_h: #if the nodes' heuristic is smaller we change that to best node and pop current node
                best_h=h
                best_node=i

        curr_node=nodes.pop(best_node)
        explored.append(curr_node)

        if on_explore is not None:
            on_explore(curr_node)

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
                        nodes.append((new_x,new_y)) #append to the quqeue
    
    if not valid_path:
        return None, 0.0, explored

    #reverse the traversed path to get the path
    path=[]
    curr=goal
    while curr is not None:
        path.append(curr)
        curr=parent[curr]
    path.reverse()

    path_cost=costs[goal]
    return path, path_cost, explored



        
        

