import heapq

class UCS:
    def __init__(self, maze):
        self.maze = maze.grid
        self.n = maze.n

    def solve(self, start=(0, 0), goal=None):
        if goal is None:
            goal = (self.n - 1, self.n - 1)

        # Priority Queue stores tuples: (cost, (x, y))
        # UCS selects the node with the lowest path cost so far (g)
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {start: None}
        cost_so_far = {start: 0}
        nodes_explored = 0
        visited = set()

        while open_set:
            # Pop the node with the lowest cost
            current_cost, current = heapq.heappop(open_set)

            # Skip if we've already processed this node (Lazy Deletion handling)
            if current in visited:
                continue
            visited.add(current)
            nodes_explored += 1

            if current == goal:
                break

            x, y = current
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy

                # Check bounds and walls
                if 0 <= nx < self.n and 0 <= ny < self.n and self.maze[nx][ny] == 0:
                    new_cost = current_cost + 1
                    
                    # If we found a cheaper path to this neighbor (or haven't seen it yet)
                    if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                        cost_so_far[(nx, ny)] = new_cost
                        came_from[(nx, ny)] = current
                        # Push to priority queue with the new cost
                        heapq.heappush(open_set, (new_cost, (nx, ny)))

        # Reconstruct path
        path = []
        cur = goal
        if cur in came_from:
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
        
        return path, nodes_explored