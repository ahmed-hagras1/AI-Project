import heapq
import math

class AStarSearch:
    def __init__(self, maze, heuristic_type="manhattan"):
        self.maze = maze.grid
        self.n = maze.n
        # Store the chosen heuristic type (default is manhattan)
        self.heuristic_type = heuristic_type.lower()

    def heuristic(self, a, b):
        """
        Calculates distance based on the selected heuristic type.
        """
        x1, y1 = a
        x2, y2 = b

        if self.heuristic_type == "manhattan":
            # Best for 4-direction grids (Up, Down, Left, Right)
            return abs(x1 - x2) + abs(y1 - y2)
        
        elif self.heuristic_type == "euclidean":
            # Shortest line distance (Good if diagonal movement was allowed)
            return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            
        elif self.heuristic_type == "chebyshev":
            # Also known as Diagonal distance (Max of dx, dy)
            return max(abs(x1 - x2), abs(y1 - y2))
            
        else:
            # If "none" or unknown, behave like Dijkstra (h=0)
            return 0

    def solve(self, start=(0, 0), goal=None):
        if goal is None:
            goal = (self.n - 1, self.n - 1)

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}
        
        nodes_explored = 0
        visited_for_count = set()

        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current in visited_for_count:
                continue
            
            visited_for_count.add(current)
            nodes_explored += 1

            if current == goal:
                break

            x, y = current
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < self.n and 0 <= ny < self.n and self.maze[nx][ny] == 0:
                    tentative_g = g_score[current] + 1

                    if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                        came_from[(nx, ny)] = current
                        g_score[(nx, ny)] = tentative_g
                        
                        # Use the dynamic heuristic method here
                        f = tentative_g + self.heuristic((nx, ny), goal)
                        heapq.heappush(open_set, (f, (nx, ny)))

        path = []
        cur = goal
        if cur in came_from:
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
        
        return path, nodes_explored