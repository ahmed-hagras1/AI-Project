import heapq

class AStarSearch:
    def __init__(self, maze):
        self.maze = maze.grid
        self.n = maze.n

    def heuristic(self, a, b):
        """
        Calculates the Manhattan distance between point a and point b.
        Formula: |x1 - x2| + |y1 - y2|
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve(self, start=(0, 0), goal=None):
        if goal is None:
            goal = (self.n - 1, self.n - 1)

        # Priority Queue stores tuples: (f_score, (x, y))
        # f_score = g_score + heuristic
        open_set = []
        heapq.heappush(open_set, (0, start))

        # Tracks where we came from for path reconstruction
        came_from = {start: None}

        # g_score: The cost of the cheapest path from start to current node
        g_score = {start: 0}

        nodes_explored = 0
        visited_for_count = set() # Just to track the number of unique nodes processed

        while open_set:
            # Get the node with the lowest f_score
            current_f, current = heapq.heappop(open_set)

            # If we already processed this node with a lower cost, skip it
            # (This handles the lazy deletion nature of heapq)
            if current in visited_for_count:
                continue
            
            visited_for_count.add(current)
            nodes_explored += 1

            if current == goal:
                break

            x, y = current
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy

                # Check bounds and walls
                if 0 <= nx < self.n and 0 <= ny < self.n and self.maze[nx][ny] == 0:
                    
                    # tentative_g is the cost to reach the neighbor through current
                    tentative_g = g_score[current] + 1

                    # If this path to neighbor is better than any previous one
                    if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                        came_from[(nx, ny)] = current
                        g_score[(nx, ny)] = tentative_g
                        
                        f = tentative_g + self.heuristic((nx, ny), goal)
                        heapq.heappush(open_set, (f, (nx, ny)))

        # Reconstruct path
        path = []
        cur = goal
        # Check if goal was actually reached
        if cur in came_from:
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
        
        return path, nodes_explored