
from typing import List, Tuple, Optional, Callable, Iterable
from collections import deque
import heapq

Coord = Tuple[int, int]

def in_bounds(grid: List[List[float]], r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def is_blocked(val) -> bool:
    return val in (1, '#', False)

def cell_cost(val) -> float:
    # If the cell stores a numeric cost > 1, use it; otherwise cost=1 for traversable cells.
    try:
        v = float(val)
        if v <= 0 or v == 1.0:  # treat 1 as wall by default; adjust if your grid differs
            return 1.0 if v == 0.0 else float("inf")
        return v
    except Exception:
        return 1.0

def walkable(grid: List[List[float]], r: int, c: int) -> bool:
    if not in_bounds(grid, r, c):
        return False
    return not is_blocked(grid[r][c])

def neighbors4(grid: List[List[float]], r: int, c: int) -> Iterable[Coord]:
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r+dr, c+dc
        if walkable(grid, nr, nc):
            yield (nr, nc)

def neighbors8(grid: List[List[float]], r: int, c: int) -> Iterable[Coord]:
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
        nr, nc = r+dr, c+dc
        if walkable(grid, nr, nc):
            yield (nr, nc)

def reconstruct_path(came_from: dict, current: Coord) -> List[Coord]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def euclidean(a: Coord, b: Coord) -> float:
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5


def find_path(grid, start: Coord, goal: Coord, *, diagonals: bool=False,
              heuristic: str="manhattan") -> tuple[list[Coord], list[Coord], float|None]:
    """
    A* pathfinding on a grid.
    Returns: (path, visited_order, total_cost). path=[] and cost=None if no path.
    Grid conventions:
      - Walls: 1, "#", or False
      - Free cell: 0 (or any non-wall). If a free cell contains a numeric >1, it is treated as its traversal cost.
    """
    if not walkable(grid, *start) or not walkable(grid, *goal):
        return [], [], None

    h_fn = manhattan if heuristic == "manhattan" else euclidean
    nbrs = neighbors8 if diagonals else neighbors4

    open_heap = []
    # entries: (f, g, counter, node)
    counter = 0
    g = {start: 0.0}
    f0 = h_fn(start, goal)
    heapq.heappush(open_heap, (f0, 0.0, counter, start))
    came_from = {}
    visited_order = []
    in_open = {start}

    while open_heap:
        _, g_curr, _, current = heapq.heappop(open_heap)
        in_open.discard(current)
        visited_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, visited_order, g_curr

        for nxt in nbrs(grid, *current):
            step = cell_cost(grid[nxt[0]][nxt[1]])
            if step == float("inf"):
                continue
            tentative_g = g_curr + step
            if tentative_g < g.get(nxt, float("inf")):
                came_from[nxt] = current
                g[nxt] = tentative_g
                f = tentative_g + h_fn(nxt, goal)
                if nxt not in in_open:
                    counter += 1
                    heapq.heappush(open_heap, (f, tentative_g, counter, nxt))
                    in_open.add(nxt)

    return [], visited_order, None
