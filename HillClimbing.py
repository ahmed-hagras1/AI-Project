class HillClimbing:
    def __init__(self, maze):
        self.maze = maze.grid
        self.n = maze.n

    def heuristic(self, a, b):
        """Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve(self, start=(0, 0), goal=None):
        if goal is None:
            goal = (self.n - 1, self.n - 1)

        current = start
        path = [current]
        visited = set([current])
        nodes_explored = 0

        while current != goal:
            nodes_explored += 1
            x, y = current
            
            # 1. Gather all valid neighbors and their heuristic scores
            neighbors = []
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                
                # Check bounds, walls, and if we've already visited it
                if (0 <= nx < self.n and 
                    0 <= ny < self.n and 
                    self.maze[nx][ny] == 0 and 
                    (nx, ny) not in visited):
                    
                    h_score = self.heuristic((nx, ny), goal)
                    neighbors.append(((nx, ny), h_score))

            # 2. If no valid neighbors exist, we are stuck (Local Maximum / Dead End)
            if not neighbors:
                return [], nodes_explored  # Failed to find path

            # 3. Sort neighbors by heuristic (lowest distance is best)
            # This is the "Greedy" part: always pick the best immediate move
            neighbors.sort(key=lambda x: x[1])

            # 4. Move to the best neighbor
            best_neighbor = neighbors[0][0]
            
            current = best_neighbor
            visited.add(current)
            path.append(current)

        return path, nodes_explored