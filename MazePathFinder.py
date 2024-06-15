from kivy.app import App
from kivy.uix.label import Label
import os
import pygame
from tkinter import Tk, filedialog
from PIL import Image
import numpy as np
import heapq


class MyApp(App):
    def build(self):
        return Label(text='Maze Path found!')

class Player:
    def __init__(self, start_pos):
        self.position = start_pos

    def move(self, direction, maze_grid):
        x, y = self.position
        if direction == 'up' and maze_grid[x - 1, y] == 0:
            self.position = (x - 1, y)
        elif direction == 'down' and maze_grid[x + 1, y] == 0:
            self.position = (x + 1, y)
        elif direction == 'left' and maze_grid[x, y - 1] == 0:
            self.position = (x, y - 1)
        elif direction == 'right' and maze_grid[x, y + 1] == 0:
            self.position = (x, y + 1)

def load_maze_image(file_path):
    img = Image.open(file_path).convert('L')  # Convert to grayscale
    img = img.point(lambda x: 0 if x < 128 else 255, '1')  # Binarize image
    maze = np.array(img, dtype=int)  # Convert to numpy array
    return maze

def convert_image_to_grid(maze_image):
    maze_grid = (maze_image == 0).astype(int)  # 0 for paths, 1 for walls
    return maze_grid

def is_goal_reached(player_pos, goal_pos):
    return player_pos == goal_pos

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1

            if 0 <= neighbor[0] < maze.shape[0]:
                if 0 <= neighbor[1] < maze.shape[1]:
                    if maze[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False

def display_maze(maze_grid, player_pos, goal_pos, path):
    pygame.init()
    cell_size = 4  # Adjust cell size to fit the entire maze on screen
    width, height = maze_grid.shape[1] * cell_size, maze_grid.shape[0] * cell_size
    screen = pygame.display.set_mode((width, height))

    player = Player(player_pos)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move('up', maze_grid)
        if keys[pygame.K_DOWN]:
            player.move('down', maze_grid)
        if keys[pygame.K_LEFT]:
            player.move('left', maze_grid)
        if keys[pygame.K_RIGHT]:
            player.move('right', maze_grid)

        screen.fill((255, 255, 255))
        for x in range(maze_grid.shape[0]):
            for y in range(maze_grid.shape[1]):
                color = (0, 0, 0) if maze_grid[x, y] == 1 else (255, 255, 255)
                pygame.draw.rect(screen, color, pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size))

        pygame.draw.rect(screen, (0, 255, 0),
                         pygame.Rect(goal_pos[1] * cell_size, goal_pos[0] * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, (255, 0, 0),
                         pygame.Rect(player.position[1] * cell_size, player.position[0] * cell_size, cell_size,
                                     cell_size))

        if path:
            for (x, y) in path:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size))

        if is_goal_reached(player.position, goal_pos):
            print("Goal Reached!")
            running = False

        pygame.display.flip()

    pygame.quit()

def main():
    # Create a Tkinter root window and hide it
    root = Tk()
    root.withdraw()

    # Open a file dialog to select a maze image
    file_path = filedialog.askopenfilename(title="Select Maze Image", filetypes=[("PNG Files", "*.png")])
    if not file_path:
        print("No file selected. Exiting...")
        return

    # Load the maze image
    maze = load_maze_image(file_path)

    # Convert the maze image to a grid
    maze_grid = convert_image_to_grid(maze)

    # Define start and goal positions
    start_pos = (1, 1)
    goal_pos = (maze_grid.shape[0] - 2, maze_grid.shape[1] - 2)

    # Find the path using A* algorithm
    path = a_star(maze_grid, start_pos, goal_pos)
    path.reverse()  # Reverse the path to start from the beginning

    # Display the maze
    display_maze(maze_grid, start_pos, goal_pos, path)

if __name__ == '__main__':
    main()
    MyApp().run()
