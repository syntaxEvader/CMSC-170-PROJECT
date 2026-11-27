# CMSC 170 Maze Pathfinding Project by Undiagnosed Heuristics
Purpose: Compare and Test different algorithms on basic grid-based mazes

## Algorithms Used
- A*
- Breadth-First Search
- Uniform Cost Search
- Greedy Best-First Search

## Information

This project compares search algorithms on grid-based mazes using Moving AI .map and .map.scen files. The movement model allows eight directions: horizontal and vertical moves cost 1, while diagonal moves cost sqrt(2). Diagonal moves that cut across blocked corners are not allowed. A* and Greedy Best-First use Octile Distance, which matches these movement costs; BFS and Uniform Cost Search do not use a heuristic. Search results can also be visualized with Matplotlib.

## Results

The program records and saves the following results to results.csv:
- Map File
- Dimensions
- Total Scenarios
- Algorithm
- Scenario (labeled from 1-5, gets the 10th 30th 50th 70th 90th percentile, to distribute scenario difficulty)
- Status
- Start Coordinates
- Goal Coordinates
- Optimal Length (optimal length based from dataset)
- Start Cell Value
- Path Cost (calculated path cost)
- Shortest Path?
- Algorithm Runtime (ms)
- Current Memory (MB)
- Peak Memory (MB)
- Explored Cells

## Requirements

- Python3
- Matplotlib

  install using:
  
  ```
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  pip install matplotlib
  ```

To run the project, do `python3 maze-reader.py`

Note: Project page redirects to a Canva website instead.
## References

[1] N. Sturtevant, “Benchmarks for Grid-Based Pathfinding,”
*Transactions on Computational Intelligence and AI in Games*,
vol. 4, no. 2, pp. 144–148, 2012.
[Online]. Available: http://web.cs.du.edu/~sturtevant/papers/benchmarks.pdf
