maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0]
]

start = (0, 0)
end = (4, 4)

def dfs(maze, start, end):
    stack = [(start, [start])]
    visited = set()

    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    while stack:
        (x, y), path = stack.pop()

        if (x, y) == end:
            return path

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
                stack.append(((nx, ny), path + [(nx, ny)]))

    return None

path = dfs(maze, start, end)
print("DFS Path:", path)

for i in range(len(maze)):
    row = ""
    for j in range(len(maze[0])):
        if (i, j) in path:
            row += "* "
        else:
            row += str(maze[i][j]) + " "
    print(row)

