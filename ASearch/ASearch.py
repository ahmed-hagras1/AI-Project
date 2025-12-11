import heapq

maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0]
]

start = (0, 0)
end = (4, 4)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, end), 0, start, [start]))
    visited = set()

    moves = [(-1,0),(1,0),(0,-1),(0,1)] 

    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current == end:
            return path

        if current in visited:
            continue
        visited.add(current)

        for dx, dy in moves:
            nx, ny = current[0] + dx, current[1] + dy

            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                new_g = g + 1
                new_f = new_g + heuristic((nx, ny), end)
                heapq.heappush(open_list, (new_f, new_g, (nx, ny), path + [(nx, ny)]))

    return None

path = astar(maze, start, end)
print("A* Path:", path)

for i in range(len(maze)):
    row = ""
    for j in range(len(maze[0])):
        if (i, j) in path:
            row += "* "
        else:
            row += str(maze[i][j]) + " "
    print(row)
