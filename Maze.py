import random

class Maze:
    def __init__(self, n, wall_prob=0.3):
        self.n = n
        self.wall_prob = wall_prob
        self.grid = self._generate_maze()

    def _generate_maze(self):
        """Generates the N x N maze grid."""
        maze = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                if random.random() < self.wall_prob:
                    row.append(1)  # wall
                else:
                    row.append(0)  # path
            maze.append(row)

        # Ensure start and goal are open
        maze[0][0] = 0
        maze[self.n-1][self.n-1] = 0
        return maze

    def print_maze(self, path=None):
        """Prints the maze to the console, optionally marking a path."""
        # Create a deep copy for printing so we don't modify the actual grid
        maze_copy = [row[:] for row in self.grid]

        if path:
            for x, y in path:
                # Check bounds to ensure path is valid before marking
                if 0 <= x < self.n and 0 <= y < self.n:
                    maze_copy[x][y] = "*"

        for row in maze_copy:
            print(" ".join(str(cell) for cell in row))
        print()