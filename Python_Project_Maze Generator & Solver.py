import pygame #pygame for showing dynamically the solution of the maze
import random
from collections import deque #It is like a list, which is used in Breadth-First Search

'''
How BFS works is by using a Queue. We have a queue of points to be reached and when we visit that point, we add all the points lying next to the point into the queue.
And this goes on till there is no more points to be reached. This was BFS algorith searches the whole area or graph.
'''

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600 #Height and Width of window
ROWS, COLS = 31, 31  # We Use odd numbers for proper maze generation
CELL_SIZE = WIDTH // COLS 
#Colors to be used later, defined in RGB values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Running the screen
pygame.display.set_caption("Maze Generator and Solver") #Title of window

# Directions for moving in the grid (used in maze generation)
DIRECTIONS = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Up, Down, Left, Right

# Function to draw the grid lines
def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

# Maze class
class Maze:
    #Since we are randomly generating a maze(using DFS), we have to create an algorith to create a maze first, then convert it into a visible form using pygame
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Initialize grid with walls (1)
        #This will create a list of values of 1 with row number and column number equal to rows and col
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]

    def generate_maze(self):
        # Start from (1, 1) to ensure proper walls around the maze
        #All the cells are givena a value of False, which means it is a wall
        stack = [(1, 1)]
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        #The first cell, ie, of row 1 and col 1 is given True value, indicating it is not a wall and is open
        visited[1][1] = True
        self.grid[1][1] = 0  # Mark starting cell as path

        while stack:
            current_cell = stack[-1] #This keeps track of current position of the cell
            neighbors = self.get_neighbors(current_cell, visited) #cehcking if there are adjacent cells to current cell which are not visited

            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_wall(current_cell, next_cell) #removing the wall to create a path to the neighbour(as we are now creating the maze)
                stack.append(next_cell) #moving on to next cell
                visited[next_cell[0]][next_cell[1]] = True
            else:
                stack.pop()

        # Call the function to add loops after generating the maze, ie, create multiple ways to solution
        self.add_loops()

#Function for finding the neighbours near the current cell.
    def get_neighbors(self, cell, visited):
        r, c = cell
        neighbors = []

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1 and not visited[nr][nc]:
                neighbors.append((nr, nc))

        return neighbors

#Function for removing the walls, ie changing values from 1 to 0
    def remove_wall(self, current, next):
        r1, c1 = current
        r2, c2 = next

        # Find the cell in between and make it a path
        wall_r, wall_c = (r1 + r2) // 2, (c1 + c2) // 2
        self.grid[r2][c2] = 0  # Mark next cell as path
        self.grid[wall_r][wall_c] = 0  # Remove wall


    def add_loops(self):
        #Randomly remove some walls to introduce loops and multiple paths.
        num_loops = random.randint(2, 60)  #Bigger the range, more the number of paths
        for _ in range(num_loops):
            r = random.randint(1, self.rows - 2)
            c = random.randint(1, self.cols - 2)

            # Ensuring we're removing a wall and not an existing path
            if self.grid[r][c] == 1 and self.has_adjacent_paths(r, c):
                self.grid[r][c] = 0

#Seeing if we can still reach the solution after modification to the maze
    def has_adjacent_paths(self, r, c):
        #Ensuring we don't break the maze structure by checking surrounding cells.
        path_count = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                path_count += 1
        return path_count >= 1  # At least one adjacent cell must be a path

#pygame code for drawing the background and walls
    def draw(self):
        for r in range(self.rows):
            for c in range(self.cols):
                color = WHITE if self.grid[r][c] == 0 else BLACK
                pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# BFS Solver, ie, the code for the BFS algorithm
def bfs(maze, start, end):
    queue = deque([start]) #using a deque type for easier modification of values
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    visited[start[0]][start[1]] = True
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #movement for the fucntion
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze.grid[nr][nc] == 0 and not visited[nr][nc]:
                queue.append((nr, nc))
                visited[nr][nc] = True
                parent[(nr, nc)] = current

    # Check if end was reached
    if end not in parent:
        return None

    # Trace back the path, if the end of one tree is reached
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path

# Draw the optimal path and highlight start/end
def draw_path_and_highlight(path, start, end):
    # Draw the path in green
    for r, c in path:
        pygame.draw.rect(screen, GREEN, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()
        pygame.time.delay(50)
    
    # Highlight the start in red and the end in blue
    pygame.draw.rect(screen, RED, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLUE, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update() #refreshing the screen

def main(): #the main function to run the program which we call
    maze = Maze(ROWS, COLS)
    maze.generate_maze()
    start = (5, 1) #here we can change the set of start and end points
    end = (ROWS - 2, COLS - 2)

    running = True
    solved = False
    path_drawn = False

    while running: #standard pygame code for quitting the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not solved:
            # Draw the maze before solving
            screen.fill(BLACK)
            maze.draw()
            draw_grid()
            pygame.display.update()

            # Run BFS to solve the maze and find the optimal path
            path = bfs(maze, start, end)
            if path is None:
                print("No path found")
            else:
                solved = True

        # Once solved, draw the path and highlight start/end only once
        if solved and not path_drawn:
            draw_path_and_highlight(path, start, end)
            path_drawn = True  # Prevent further updates and overwriting

    pygame.quit()

#Running the program
main()
