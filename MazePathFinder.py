
"""
Minimal CLI to run grid pathfinding with BFS/DFS/Dijkstra/A*.

Usage examples:
  python mazepathfinder.py --algo bfs
  python mazepathfinder.py --algo dijkstra --diagonals
  python mazepathfinder.py --algo astar --heuristic manhattan

By default it uses an embedded demo grid. You can pass --grid path/to/file.txt
where the file contains rows of 0 and 1 (space or comma-separated). 1 = wall, 0 = free.
Optionally cells may contain weights like 5 meaning entering that cell costs 5.
"""
import argparse
from typing import List

import bfs
import dfs
import dijkstra
import a_star

def parse_grid_file(path: str) -> List[List[float]]:
    grid = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p for p in line.replace(",", " ").split() if p]
            row = []
            for p in parts:
                try:
                    row.append(float(p))
                except Exception:
                    row.append(0.0 if p in (".","0") else 1.0 if p in ("#","1") else 0.0)
            grid.append(row)
    if not grid:
        raise ValueError("Empty grid from file")
    w = max(len(r) for r in grid)
    for r in grid:
        if len(r) < w:
            r.extend([1.0]*(w-len(r)))  # pad with walls
    return grid

def demo_grid() -> List[List[float]]:
    # 0 free, 1 wall
    return [
        [0,0,0,0,0,1,0,0,0,0],
        [1,1,0,1,0,1,0,1,1,0],
        [0,0,0,1,0,0,0,1,0,0],
        [0,1,0,0,0,1,0,0,0,1],
        [0,1,0,1,0,1,0,1,0,0],
        [0,1,0,1,0,0,0,1,0,0],
        [0,0,0,1,1,1,0,1,0,0],
        [0,1,0,0,0,0,0,1,0,1],
        [0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,0],
    ]

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--algo", choices=["bfs","dfs","dijkstra","astar"], default="bfs")
    ap.add_argument("--grid", type=str, help="Path to grid file (0=free, 1=#, or numeric weights)")
    ap.add_argument("--start", type=int, nargs=2, metavar=("R","C"), default=(0,0))
    ap.add_argument("--goal", type=int, nargs=2, metavar=("R","C"), default=(9,9))
    ap.add_argument("--diagonals", action="store_true", help="Allow 8-direction moves")
    ap.add_argument("--heuristic", choices=["manhattan","euclidean"], default="manhattan",
                    help="Heuristic for A*")

    args = ap.parse_args(argv)

    grid = parse_grid_file(args.grid) if args.grid else demo_grid()
    start, goal = tuple(args.start), tuple(args.goal)

    if args.algo == "bfs":
        path, visited, cost = bfs.find_path(grid, start, goal, diagonals=args.diagonals)
    elif args.algo == "dfs":
        path, visited, cost = dfs.find_path(grid, start, goal, diagonals=args.diagonals)
    elif args.algo == "dijkstra":
        path, visited, cost = dijkstra.find_path(grid, start, goal, diagonals=args.diagonals)
    else:
        path, visited, cost = a_star.find_path(grid, start, goal, diagonals=args.diagonals, heuristic=args.heuristic)

    print(f"Algorithm: {args.algo}")
    print(f"Visited: {len(visited)} nodes")
    if path:
        print(f"Path length: {len(path)-1}  Total cost: {cost}")
        print("Path:", path)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
