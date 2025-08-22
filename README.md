# Maze Path Finder
Simple maze path finder
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Open Source](https://img.shields.io/badge/Open%20Source-✓-success)

A Python-based tool for finding optimal paths through maze images using various pathfinding algorithms. This application processes maze images, identifies start and end points, and computes the shortest path using algorithms like A*, Dijkstra, and BFS.

## Features

- 🖼️ **Image Processing**: Converts maze images into traversable grids
- 🧭 **Multiple Algorithms**: Supports A*, Dijkstra, BFS, and DFS pathfinding
- 🎯 **Automatic Detection**: Identifies start and end points in mazes
- 📊 **Visualization**: Generates visual representations of the pathfinding process
- ⚡ **Performance Metrics**: Measures algorithm efficiency and path optimality

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Basic Usage
```bash
python MazePathFinder.py --input examples/maze.png --algorithm astar --output examples/solution.png
```
# Uses an embedded demo grid:

```bash
python mazepathfinder.py --algo bfs
python mazepathfinder.py --algo dijkstra --diagonals
python mazepathfinder.py --algo astar --heuristic manhattan
```
# Or run on your own file (0=free, 1=#, or numeric weights):

```bash
python mazepathfinder.py --algo astar --grid path/to/grid.txt --start 0 0 --goal 9 9
```
## Supported Algorithms

| Algorithm | Optimal | Complete |  Best For |
|-----------|---------|----------|----------|
| A* Search | ✓ | ✓ | Most mazes with heuristic |
| Dijkstra's | ✓ | ✓ | Weighted mazes |
| BFS | ✓ | ✓ | Unweighted mazes |
| DFS | ✗ | ✓ | Memory-constrained cases |

## Examples

### Input Maze
![Input Maze](examples/maze.png)

### Solved Maze
![Solved Maze](examples/solution.png)

## Advanced Usage

```python
from maze_solver import MazeSolver

# Initialize solver
solver = MazeSolver('maze.png')

# Solve using specific algorithm
path = solver.solve(algorithm='astar', heuristic='manhattan')

# Save solution
solver.save_solution('solution.png')

# Get performance metrics
stats = solver.get_statistics()
print(f"Path length: {stats['path_length']}")
print(f"Time taken: {stats['time_taken']} seconds")
print(f"Nodes explored: {stats['nodes_explored']}")
```

## Configuration Options

- `--algorithm`: Choose pathfinding algorithm (astar, dijkstra, bfs, dfs)
- `--heuristic`: For A* algorithm (manhattan, euclidean, chebyshev)
- `--animate`: Generate animation of solving process
- `--speed`: Animation speed (1-10)
- `--output-format`: Output image format (png, jpg, gif)

## Project Structure

```
MazePathFinder/
├── MazePathFinder.py     # Main solver class
├── algorithms/        # Pathfinding implementations
├── utils/             # Image processing utilities
├── examples/          # Sample mazes and solutions
├── tests/             # Unit tests
└── requirements.txt   # Dependencies
```

## Contributing

We welcome contributions! Please check the issue tracker for existing issues and feel free to submit new ones, feature requests, or pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by various pathfinding visualizations and educational resources
- Uses Pillow for image processing
- Icons from Shields.io for badges

## Support

If you encounter any problems or have questions, please open an issue on GitHub.

---

<p align="center">
Made with ❤️ and Python
</p>
