import heapq

class GreedyBFS:
    def __init__(self, maze):
        self.maze = maze.grid
        self.n = maze.n

    def heuristic(self, a, b):
        """
        Manhattan distance.
        Greedy Best-First Search uses ONLY this to decide where to go.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve(self, start=(0, 0), goal=None):
        if goal is None:
            goal = (self.n - 1, self.n - 1)

        # Priority Queue stores tuples: (heuristic_cost, (x, y))
        open_set = []
        # We start with the heuristic distance of the start node
        heapq.heappush(open_set, (self.heuristic(start, goal), start))

        came_from = {start: None}
        visited = set([start])
        nodes_explored = 0

        found = False

        while open_set:
            # Pop the node that is estimated to be CLOSEST to the goal
            _, current = heapq.heappop(open_set)
            
            nodes_explored += 1

            if current == goal:
                found = True
                break

            x, y = current
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy

                # Check bounds and walls
                if 0 <= nx < self.n and 0 <= ny < self.n and self.maze[nx][ny] == 0:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        came_from[(nx, ny)] = current
                        
                        # Calculate priority based ONLY on heuristic (Greedy)
                        h_score = self.heuristic((nx, ny), goal)
                        heapq.heappush(open_set, (h_score, (nx, ny)))

        # Reconstruct path
        path = []
        if found:
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
        
        return path, nodes_explored