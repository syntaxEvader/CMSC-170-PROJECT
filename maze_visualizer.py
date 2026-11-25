import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap

def animate_search(
    grid, start, goal, path, path_cost, explored_cells, information
):
    # Animate a completed search result without rerunning the algorithm.

    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        return path, path_cost, explored_cells

    height = len(grid) # number of rows
    width = len(grid[0]) # number of columns

    for x, y in (start, goal):
        if not (0 <= x < width and 0 <= y < height) or grid[y][x] != 0:
            return path, path_cost, explored_cells

    explored = [[False] * width for _ in range(height)] # boolean grid to track explored cells
    visible_explored_cells = []
    display_grid = [row[:] for row in grid]
    display_grid[start[1]][start[0]] = 2
    display_grid[goal[1]][goal[0]] = 3

    figure, (axis, variables_axis) = plt.subplots(
        1, 2, figsize=(11, 6), gridspec_kw={"width_ratios": [3, 1]}
    )
    color_map = ListedColormap(
        ["white", "#263238", "black", "red", "#9C9C9C", "gray", "#c5c5c5"]
    )
    image = axis.imshow(
        display_grid,
        cmap=color_map,
        norm=BoundaryNorm(range(8), color_map.N),
    )
    axis.axis("off")
    path_outline, = axis.plot([], [], color="#263238", linewidth=2.5, zorder=3)
    path_line, = axis.plot([], [], color="green", linewidth=2.5, zorder=4)
    axis.scatter(
        [start[0], goal[0]],
        [start[1], goal[1]],
        c=["black", "red"],
        edgecolors="white",
        linewidths=2,
        s=100,
        zorder=5,
    )
    variables_axis.set_title("Information", loc="left")
    variables_axis.set_xticks([])
    variables_axis.set_yticks([])
    for spine in variables_axis.spines.values():
        spine.set_color("#b0bec5")
    display_information = information.copy()
    display_information[-1] = "Explored Cells: 0"
    information_text = variables_axis.text(
        0.05,
        0.95,
        "\n".join(display_information),
        transform=variables_axis.transAxes,
        va="top",
        fontsize=9,
    )
    variables_axis.text(
        0.05,
        0.15,
        "to get the information, \nthis algorithm is run once \nbefore this visualizer is opened ."
    )
    path_found = False
    plt.ion()
    plt.pause(0.0005)

    def redraw(): # Redraws the display with the current explored cells and path.
        display = [row[:] for row in grid]
        for cell in visible_explored_cells:
            display[cell[1]][cell[0]] = 6 if path_found else 4
        display[start[1]][start[0]] = 2
        display[goal[1]][goal[0]] = 3
        image.set_data(display)
        display_information[-1] = (
            "Explored Cells: " + str(len(visible_explored_cells))
        )
        information_text.set_text("\n".join(display_information))
        figure.canvas.draw_idle()
        plt.pause(0.0005)
        return display

    for cell in explored_cells:
        x = cell[0]
        y = cell[1]
        if not explored[y][x]:
            explored[y][x] = True
            visible_explored_cells.append(cell)
        count = len(visible_explored_cells)
        if (count < 173 and count % 7 == 0) or (count % 377 == 0 and (count < 12133 and count > 237)) or count % 2137 == 0:
            redraw()

    path_found = bool(path)
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
        plt.pause(0.0005)

    draw_path_line(path, reaches_goal=True)

    plt.ioff()
    plt.show()
    return path, path_cost, explored_cells
