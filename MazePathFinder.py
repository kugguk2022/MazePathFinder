
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import numpy as np
import pygame
from typing import Tuple, List

# Import the algorithm modules placed next to this script
import a_star
import bfs
import dfs
import dijkstra

Coord = Tuple[int, int]

# ---------------------- Image / Grid utils ----------------------
def load_maze_image(file_path: str) -> np.ndarray:
    """
    Load image, convert to 1-bit (paths/walls), return numpy array with 0 (path) and 1 (wall).
    """
    img = Image.open(file_path).convert('L')
    # binarize: <128 -> black (0), else white (255)
    img = img.point(lambda x: 0 if x < 128 else 255, '1')
    maze = np.array(img, dtype=int)
    # Convert to grid convention: 0 for free, 1 for wall -> already integer 0/1
    return maze

def numpy_to_grid_list(maze_np: np.ndarray) -> List[List[float]]:
    """
    Convert numpy 0/1 array into a list-of-lists for the algorithm modules.
    0 -> free (cost 1), 1 -> wall.
    """
    # Cast to int then to Python lists
    return maze_np.astype(int).tolist()

# ---------------------- Pygame visualizer ----------------------
def display_maze(maze_grid_np: np.ndarray, start: Coord, goal: Coord, path: List[Coord],
                 cell_size: int = 6, show_path=True):
    """
    Blocking visualization window using pygame. Arrow keys move a red 'player' square.
    """
    pygame.init()
    H, W = maze_grid_np.shape
    width, height = W * cell_size, H * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("MazePathFinder")

    # Player
    player = list(start)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player[0] > 0 and maze_grid_np[player[0]-1, player[1]] == 0:
            player[0] -= 1
        if keys[pygame.K_DOWN] and player[0] < H-1 and maze_grid_np[player[0]+1, player[1]] == 0:
            player[0] += 1
        if keys[pygame.K_LEFT] and player[1] > 0 and maze_grid_np[player[0], player[1]-1] == 0:
            player[1] -= 1
        if keys[pygame.K_RIGHT] and player[1] < W-1 and maze_grid_np[player[0], player[1]+1] == 0:
            player[1] += 1

        # Draw
        screen.fill((255, 255, 255))
        # Walls/paths
        for r in range(H):
            y = r * cell_size
            row = maze_grid_np[r]
            for c in range(W):
                x = c * cell_size
                if row[c] == 1:
                    pygame.draw.rect(screen, (0,0,0), (x, y, cell_size, cell_size))

        # Optional path
        if show_path and path:
            for (r, c) in path:
                pygame.draw.rect(screen, (0, 0, 255), (c*cell_size, r*cell_size, cell_size, cell_size))

        # Start, Goal, Player
        pygame.draw.rect(screen, (255, 165, 0), (start[1]*cell_size, start[0]*cell_size, cell_size, cell_size))  # start = orange
        pygame.draw.rect(screen, (0, 200, 0), (goal[1]*cell_size, goal[0]*cell_size, cell_size, cell_size))        # goal = green
        pygame.draw.rect(screen, (200, 0, 0), (player[1]*cell_size, player[0]*cell_size, cell_size, cell_size))    # player = red

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# ---------------------- Tkinter App ----------------------
class MazePathFinderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MazePathFinder (Tk + Pygame)")
        self.geometry("520x320")
        self.resizable(False, False)

        # State
        self.file_path = tk.StringVar(value="")
        self.algo = tk.StringVar(value="A*")
        self.heuristic = tk.StringVar(value="manhattan")
        self.diagonals = tk.BooleanVar(value=False)
        self.cell_size = tk.IntVar(value=6)
        self.start_str = tk.StringVar(value="1,1")
        self.goal_str = tk.StringVar(value="auto")  # auto -> (H-2, W-2)
        self.show_path = tk.BooleanVar(value=True)

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 8, "pady": 6}

        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, **pad)

        # File row
        row1 = ttk.Frame(frm)
        row1.pack(fill="x", **pad)
        ttk.Label(row1, text="Maze image:").pack(side="left")
        ttk.Entry(row1, textvariable=self.file_path, width=44).pack(side="left", padx=6)
        ttk.Button(row1, text="Browse...", command=self._browse).pack(side="left")

        # Algo row
        row2 = ttk.Frame(frm)
        row2.pack(fill="x", **pad)
        ttk.Label(row2, text="Algorithm:").pack(side="left")
        ttk.Combobox(row2, textvariable=self.algo, values=["A*","Dijkstra","BFS","DFS"], width=10, state="readonly").pack(side="left", padx=6)

        ttk.Checkbutton(row2, text="Diagonals (8-neigh)", variable=self.diagonals).pack(side="left", padx=10)

        # Heuristic row (for A* only)
        row3 = ttk.Frame(frm)
        row3.pack(fill="x", **pad)
        ttk.Label(row3, text="A* Heuristic:").pack(side="left")
        ttk.Combobox(row3, textvariable=self.heuristic, values=["manhattan","euclidean"], width=12, state="readonly").pack(side="left", padx=6)
        ttk.Checkbutton(row3, text="Show path overlay", variable=self.show_path).pack(side="left", padx=10)

        # Start/Goal row
        row4 = ttk.Frame(frm)
        row4.pack(fill="x", **pad)
        ttk.Label(row4, text="Start (r,c):").pack(side="left")
        ttk.Entry(row4, textvariable=self.start_str, width=10).pack(side="left", padx=6)
        ttk.Label(row4, text="Goal (r,c or 'auto') :").pack(side="left")
        ttk.Entry(row4, textvariable=self.goal_str, width=10).pack(side="left", padx=6)

        # Display row
        row5 = ttk.Frame(frm)
        row5.pack(fill="x", **pad)
        ttk.Label(row5, text="Cell size:").pack(side="left")
        ttk.Spinbox(row5, from_=2, to=40, textvariable=self.cell_size, width=6).pack(side="left", padx=6)

        # Buttons
        row_btn = ttk.Frame(frm)
        row_btn.pack(fill="x", **pad)
        ttk.Button(row_btn, text="Run Pathfinding", command=self._run).pack(side="left")
        ttk.Button(row_btn, text="Quit", command=self.destroy).pack(side="right")

        # Hint
        hint = ttk.Label(frm, foreground="#666",
            text="Tip: white pixels = free (0), black = wall (1). Start defaults to (1,1), Goal to (H-2,W-2).")
        hint.pack(fill="x", **pad)

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Select Maze Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files","*.*")]
        )
        if path:
            self.file_path.set(path)

    def _parse_rc(self, s: str) -> Coord | None:
        try:
            r_str, c_str = s.split(",")
            return (int(r_str.strip()), int(c_str.strip()))
        except Exception:
            return None

    def _run(self):
        if not self.file_path.get():
            messagebox.showwarning("No image", "Please choose a maze image first.")
            return
        try:
            maze_np = load_maze_image(self.file_path.get())
        except Exception as e:
            messagebox.showerror("Failed to load image", f"{e}")
            return

        H, W = maze_np.shape
        start = self._parse_rc(self.start_str.get()) or (1,1)
        goal = (H-2, W-2) if self.goal_str.get().strip().lower() == "auto" else self._parse_rc(self.goal_str.get())
        if goal is None:
            messagebox.showerror("Invalid goal", "Goal must be 'auto' or 'r,c' integers.")
            return

        # Sanity checks
        def inside(rc: Coord): return 0 <= rc[0] < H and 0 <= rc[1] < W
        if not (inside(start) and inside(goal)):
            messagebox.showerror("Out of bounds", "Start or Goal outside maze.")
            return
        if maze_np[start[0], start[1]] == 1 or maze_np[goal[0], goal[1]] == 1:
            messagebox.showerror("Blocked", "Start/Goal is a wall. Choose different coordinates.")
            return

        grid_list = numpy_to_grid_list(maze_np)

        # Dispatch
        algo = self.algo.get()
        diags = self.diagonals.get()
        path, visited, cost = [], [], None
        try:
            if algo == "A*":
                path, visited, cost = a_star.find_path(grid_list, start, goal, diagonals=diags, heuristic=self.heuristic.get())
            elif algo == "Dijkstra":
                path, visited, cost = dijkstra.find_path(grid_list, start, goal, diagonals=diags)
            elif algo == "BFS":
                path, visited, cost = bfs.find_path(grid_list, start, goal, diagonals=diags)
            else:
                path, visited, cost = dfs.find_path(grid_list, start, goal, diagonals=diags)
        except Exception as e:
            messagebox.showerror("Pathfinding error", f"{e}")
            return

        if not path:
            messagebox.showinfo("No Path", "No path found with the selected settings.")
        else:
            steps = len(path) - 1 if cost is None else cost
            messagebox.showinfo("Path found", f"Visited: {len(visited)} nodes\nPath length/cost: {steps}")

        # Show pygame window with overlay
        self.withdraw()
        try:
            display_maze(maze_np, start, goal, path, cell_size=int(self.cell_size.get()), show_path=self.show_path.get())
        finally:
            self.deiconify()

def main():
    app = MazePathFinderApp()
    app.mainloop()

if __name__ == "__main__":
    main()
