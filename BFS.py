from collections import deque

class BFS:
    def __init__(self, maze):
        self.maze = maze.grid
        self.n = maze.n

    def solve(self, start=(0, 0), goal=None):
        if goal is None:
            goal = (self.n - 1, self.n - 1)

        queue = deque([start])
        visited = set([start])
        parent = {start: None}
        nodes_explored = 0

        while queue:
            current = queue.popleft()
            nodes_explored += 1

            if current == goal:
                break

            x, y = current
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy

                if (
                    0 <= nx < self.n and
                    0 <= ny < self.n and
                    self.maze[nx][ny] == 0 and
                    (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    parent[(nx, ny)] = current
                    queue.append((nx, ny))

        # reconstruct path
        path = []
        cur = goal
        while cur is not None and cur in parent:
            path.append(cur)
            cur = parent[cur]
        path.reverse()

        return path, nodes_explored