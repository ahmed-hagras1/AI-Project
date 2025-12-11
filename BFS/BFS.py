from collections import deque

def FindWayBFS(Maze, Start, Goal):
    Rows =len(Maze)
    Columns =len(Maze[0])
    queue =deque([Start])
    LastStep =set([Start])
    StepTrue ={Start:None}
    Direction =[(1,0), (-1,0), (0,1), (0,-1)]
    while queue:
        x, y =queue.popleft()
        if (x, y) == Goal:
            path = []
            cur =(x, y)
            while cur is not None:
                path.append(cur)
                cur = StepTrue[cur]
            return path[::-1]

        for n, s in Direction:
            e, w = x + n, y + s
            if 0 <= e < Rows and 0 <= w < Columns and Maze[e][w] != 1:
                if (e, w) not in LastStep:
                    LastStep.add((e, w))
                    StepTrue[(e, w)] = (x, y)
                    queue.append((e, w))
Maze = [ [  0 ,1, 0 ,0, 0 ,1, 0  ],

         [  0 ,1, 0 ,1, 0 ,1, 0  ],

         [  0 ,1, 0 ,1, 0 ,1, 0  ],

         [  0 ,1, 0 ,1, 0 ,1, 0  ],

         [  0 ,0, 0 ,1, 0 ,0, 0  ] ]

Start = (0, 0)
Goal  = (0, 6)


Way = FindWayBFS(Maze, Start, Goal)
print(Way)