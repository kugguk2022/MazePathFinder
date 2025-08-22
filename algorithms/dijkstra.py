
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


def find_path(grid, start: Coord, goal: Coord, *, diagonals: bool=False) -> tuple[list[Coord], list[Coord], float|None]:
    """
    Dijkstra shortest path on weighted grid (non-negative costs).
    Returns: (path, visited_order, total_cost). path=[] and cost=None if no path.
    """
    if not walkable(grid, *start) or not walkable(grid, *goal):
        return [], [], None

    nbrs = neighbors8 if diagonals else neighbors4
    dist = {start: 0.0}
    pq = [(0.0, start)]
    visited_order = []
    came_from = {}
    seen = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        visited_order.append(u)
        if u == goal:
            return reconstruct_path(came_from, u), visited_order, d

        for v in nbrs(grid, *u):
            step = cell_cost(grid[v[0]][v[1]])
            if step == float("inf"):
                continue
            nd = d + step
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                came_from[v] = u
                heapq.heappush(pq, (nd, v))

    return [], visited_order, None
