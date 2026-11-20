# Imports
import os
import time
import tracemalloc
from astar import a_star                                  # later when i push
from maze_visualizer import animate_search
from bfs import bfs

map_folder = "maze-map"                                     # Folder containing all .map files
scen_folder = "maze-scen"                                   # Folder containing all .map.scen files

map_files = sorted(os.listdir(map_folder))                  # .map files in alphabetical order (?)

# Function Definitions

# This function reads the .map file and converts it into a 2D grid
def read_map(file_name):
    map_file = open(file_name, "r")                         # Opens the .map file for reading
    lines = map_file.readlines()                            # Reads all lines from the file
    map_file.close()

    # Extracts the height and width from the file header
    height = int(lines[1].strip().split()[1])
    width = int(lines[2].strip().split()[1])

    grid = []                                               # 2D list representing the maze layout

    # Reads from row 4 of file, after the word "map"
    for i in range(4, 4 + height):
        raw_row = lines[i].strip()                          # Removes trailing newline characters
        grid_row = []                                       # List representing a single row of cells

        # basically 0 is a walkable block or space, and 1 is a wall
        for cell in raw_row:
            if cell == "@":
                grid_row.append(1)                          # Wall
            else:
                grid_row.append(0)                          # Walkable space ('.')

        grid.append(grid_row)                               # Adds the row to the 2D grid

    return grid, width, height

# This function reads the .scen file and gets the start and goal coordinates
def read_scenarios(file_name):
    scen_file = open(file_name, "r")                        # Opens the .scen file for reading
    lines = scen_file.readlines()                           # Reads all lines from the file
    scen_file.close()

    scenarios = []                                          # List of all test cases from the scenario file

    # Reads from line 1 (after the version)
    for i in range(1, len(lines)):
        line = lines[i].strip()

        # Skips any empty lines
        if not line:
            continue

        columns = line.split()                              # Splits line into columns

        # Assigns the initial coordinates, goal coordinates, and optimal path length
        initial_x = int(columns[4])
        initial_y = int(columns[5])
        goal_x = int(columns[6])
        goal_y = int(columns[7])
        optimal_length = float(columns[8])

        # Stores the scenario details as a tuple
        start_loc = (initial_x, initial_y)
        goal_loc = (goal_x, goal_y)
        scenarios.append((start_loc, goal_loc, optimal_length))

    return scenarios


# Test print
def test_if_gumagana(map_name, grid, width, height, scenarios, algorithm_name, algorithm):
    print("\n====================\n")

    print("Map File:", map_name)
    print("Dimensions:", str(width) + " x " + str(height))
    print("Algorithm:", algorithm_name)
    print("Total Scenarios: " + str(len(scenarios)))

    print("\nFirst 5 Scenarios:")

    # 10th 30th 50th 70th 90th percentile
    used_scenarios = []
    sample_count = min(5, len(scenarios))
    for i in range(sample_count):
        used_scenarios.append(scenarios[i * len(scenarios) // sample_count])

    for i in range(len(used_scenarios)):
        if i >= len(scenarios):
            break

        start_loc, goal_loc, optimal_length = used_scenarios[i]

        start_x = start_loc[0]
        start_y = start_loc[1]

        cell_value = grid[start_y][start_x]

        algorithm_start = time.perf_counter()
        path, path_cost, explored = algorithm(grid, start_loc, goal_loc)
        runtime_seconds = time.perf_counter() - algorithm_start

        tracemalloc.start()
        try:
            memory_result = algorithm(grid, start_loc, goal_loc)
            current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        del memory_result

        information = [] #store output info inside an array for printing and visualizer
        if path is None:
            path = []
            information.extend([
                "No path found.",
                "-- Scenario " + str(i+1) + " --",
                "Start Coordinates: " + str(start_loc),
                "Goal Coordinates: " + str(goal_loc),
                "Expected Optimal Length: " + ("No path" if optimal_length < 0 else str(optimal_length)),
                "Start Cell Value: " + ("Walkable" if cell_value == 0 else "Wall"),
                "Path Cost: N/A",
                "Shortest Path?: N/A",
            ])
        else:
            information.extend([
                "-- Scenario " + str(i+1) + " --",
                "Start Coordinates: " + str(start_loc),
                "Goal Coordinates: " + str(goal_loc),
                "Optimal Length: " + str(optimal_length),
                "Start Cell Value: " + "Walkable" if cell_value == 0 else "Wall",
                "Path Cost: " + str(path_cost),
                "Shortest Path?" + "Yes\n" if path_cost == optimal_length else "No\n"
            ])
        information.extend([
            "Algorithm Runtime: {:.6f} ms".format(runtime_seconds * 1000),
            f"Memory Usage: (current) {current / 10**6:.4f} MB\n (peak) {peak / 10**6:.4f} MB",
            "Explored Cells: " + str(len(explored)),
        ])

        for line in information:
            print(line)
        print()
        animate_search(
            grid, start_loc, goal_loc, path, path_cost, explored, information
        )

        # Checks if the starting coordinate is walkable (0 = open path, 1 = wall)


    print("====================\n")

# Loops through every single file in the maze-map folder
def main_loop():
    for map_file_name in map_files:
        # In case may maligaw na hindi .map file
        if not map_file_name.endswith(".map"):
            continue

        map_path = map_folder + "/" + map_file_name             # Builds the full path for the .map file
        scen_path = scen_folder + "/" + map_file_name + ".scen" # Builds the matching .map.scen file path

        # Checks if the matching scenario file exists before reading
        if not os.path.exists(scen_path):
            print("Warning: Missing scenario file for", map_file_name)
            continue

        map_results = read_map(map_path)                        # Reads the maze grid file

        # Hiwalayin ang results
        grid = map_results[0]
        width = map_results[1]
        height = map_results[2]

        scenarios = read_scenarios(scen_path)                   # Reads the scenario test cases

        # Testing testing things just got more interesting
        test_if_gumagana(
            map_file_name, grid, width, height, scenarios, "A*", a_star
        )
        break


def choose_algorithm(): # function for choosing search algorithm
    while True:
        print("\nChoose an algorithm:")
        print("1. A*")
        print("2. Uniform Cost Search (not implemented yet)")
        print("3. Breadth-First Search")
        print("4. Greedy Algorithm (not implemented yet)")
        print("0. Exit")

        choice = input("Enter a number: ").strip()
        if choice == "0":
            return None, None
        if choice == "1":
            return "A*", a_star
        elif choice=="3":
            return "Breadth-First Seach",bfs
        elif choice in ("2", "4"):
            algorithm_names = {
                "2": "Uniform Cost Search",
                "3": "Breadth-First Search",
                "4": "Greedy Algorithm",
            }
            print(algorithm_names[choice], "is not implemented yet.")
            continue
        else:
            print("Invalid choice.")


def main_menu():
    algorithm_name, algorithm = choose_algorithm()
    if algorithm is None:
        return

    map_files = sorted(
        file_name for file_name in os.listdir(map_folder)
        if file_name.endswith(".map")
    )
    if not map_files:
        print("No .map files found in", map_folder)
        return

    print("Choose a map:")
    for index, file_name in enumerate(map_files, start=1):
        print(str(index) + ".", file_name)

    while True:
        choice = input("Enter a number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(map_files):
            map_file_name = map_files[int(choice) - 1]
            map_path = os.path.join(map_folder, map_file_name)
            scen_path = os.path.join(scen_folder, map_file_name + ".scen")
            if not os.path.exists(scen_path):
                print("Warning: Missing scenario file for", map_file_name)
                continue
    
            map_results = read_map(map_path)                        # Reads the maze grid file
    
            # Hiwalayin ang results
            grid = map_results[0]
            width = map_results[1]
            height = map_results[2]
    
            scenarios = read_scenarios(scen_path)                   # Reads the scenario test cases
    
            # Testing testing things just got more interesting
            test_if_gumagana(map_file_name, grid, width, height, scenarios, algorithm_name, algorithm)
            return
        print("Invalid choice. Enter a number from 1 to", len(map_files))

main_menu()
