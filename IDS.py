class IDS:
    def __init__(self, maze):
        self.maze = maze.grid
        self.n = maze.n

    def solve(self, start=(0, 0), goal=None):
        """
        Main IDS loop: increases depth limit until goal is found or max depth reached.
        """
        if goal is None:
            goal = (self.n - 1, self.n - 1)

        total_nodes_explored = 0
        depth_limit = 0
        
        # Safety break: Max depth theoretically needed is total cells (N*N)
        max_limit = self.n * self.n

        while depth_limit <= max_limit:
            # Run DLS for the current depth limit
            found_path, count = self._dls(start, goal, depth_limit)
            
            total_nodes_explored += count

            if found_path:
                return found_path, total_nodes_explored
            
            depth_limit += 1

        return [], total_nodes_explored

    def _dls(self, start, goal, limit):
        """
        Performs Depth-Limited Search (Iterative approach).
        Returns: (path_list, nodes_explored_count)
        """
        # Stack stores tuples: (current_node, path_so_far)
        stack = [(start, [start])]
        nodes_explored = 0
        
        # To handle cycles efficiently in DLS: track the best depth we've seen a node
        # If we reach a node again at a deeper/same level in the SAME iteration, skip it.
        visited_depths = {start: 0}

        while stack:
            current, path = stack.pop()
            nodes_explored += 1
            
            if current == goal:
                return path, nodes_explored
            
            # If we reached the limit, do not expand further
            if len(path) - 1 >= limit:
                continue

            x, y = current
            # Explore neighbors
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < self.n and 0 <= ny < self.n and self.maze[nx][ny] == 0:
                    new_depth = len(path) # Path length is current_depth + 1
                    
                    # Optimization: Only push if we haven't visited this node 
                    # at a shallower depth in this specific DLS run.
                    if (nx, ny) not in visited_depths or new_depth < visited_depths[(nx, ny)]:
                        visited_depths[(nx, ny)] = new_depth
                        stack.append(((nx, ny), path + [(nx, ny)]))
        
        return None, nodes_explored