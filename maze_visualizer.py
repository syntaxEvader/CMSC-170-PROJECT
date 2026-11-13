import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def animate_search(grid, start, goal, algorithm):
    # Run a search algorithm and animate explored regions and its path.

    # validation checks
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        path, path_cost, _ = algorithm(grid, start, goal, None)
        return path, path_cost, []

    height = len(grid) # number of rows
    width = len(grid[0]) # number of columns

    for x, y in (start, goal):
        if not (0 <= x < width and 0 <= y < height) or grid[y][x] != 0:
            path, path_cost, _ = algorithm(grid, start, goal, None)
            return path, path_cost, []

    explored = [[False] * width for _ in range(height)] # boolean grid to track explored cells
    explored_cells = [] # linear array to store explored cells
    display_grid = [row[:] for row in grid]
    display_grid[start[1]][start[0]] = 2
    display_grid[goal[1]][goal[0]] = 3

    figure, axis = plt.subplots()
    image = axis.imshow(
        display_grid,
        cmap=ListedColormap(
            ["white", "#263238", "black", "red", "yellow", "gray"]
        ),
    )
    axis.axis("off")
    path_outline, = axis.plot([], [], color="#263238", linewidth=2.5, zorder=3)
    path_line, = axis.plot([], [], color="green", linewidth=2.5, zorder=4)
    plt.ion()
    plt.pause(0.01)

    def redraw(): # Redraws the display with the current explored cells and path.
        display = [row[:] for row in grid]
        for cell in explored_cells:
            display[cell[1]][cell[0]] = 4
        display[start[1]][start[0]] = 2
        display[goal[1]][goal[0]] = 3
        image.set_data(display)
        figure.canvas.draw_idle()
        plt.pause(0.001)
        return display

    def on_explore(cell): # mark cell as explored and redraw the display
        x = cell[0]
        y = cell[1]
        if not explored[y][x]:
            explored[y][x] = True
            explored_cells.append([x, y])
        count = len(explored_cells)
        if count <= 20 or count % 2000 == 0:
            redraw()

    path, path_cost, _ = algorithm(grid, start, goal, on_explore)
    display = redraw()
    chunk_size = max(1, len(path) // 100) 


    # after the path is found, draws the path line on the display
    def draw_path_line(visible_path, reaches_goal): 
        xs = []
        ys = []
        for cell in visible_path:
            xs.append(cell[0])
            ys.append(cell[1])

        if reaches_goal and len(visible_path) > 1:
            previous = visible_path[-2]
            goal_cell = visible_path[-1]
            xs[-1] = (previous[0] + goal_cell[0]) / 2
            ys[-1] = (previous[1] + goal_cell[1]) / 2
        path_outline.set_data(xs, ys)
        path_line.set_data(xs, ys)

    for end in range(2, len(path) + 1, chunk_size):
        visible_path = path[:end]
        for index in range(1, len(visible_path) - 1):
            x = visible_path[index][0]
            y = visible_path[index][1]
            display[y][x] = 5
        image.set_data(display)
        draw_path_line(visible_path, end >= len(path))
        figure.canvas.draw_idle()
        plt.pause(0.005)

    draw_path_line(path, reaches_goal=True)

    plt.ioff()
    plt.show()
    return path, path_cost, explored_cells
