import time
from Maze import Maze
from BFS import BFS    
from DFS import DFS
from AStarSearch import AStarSearch
from UCS import UCS
from IDS import IDS
from HillClimbing import HillClimbing
from GeneticAlgorithm import GeneticAlgorithm
from GreedyBFS import GreedyBFS

# 1. Setup Maze
maze = Maze(10, wall_prob=0.3)
start = (0, 0)
goal = (maze.n - 1, maze.n - 1)

print("Generated Maze:")
maze.print_maze()

print("=== Results ===")

# ----------------- BFS Section -----------------
bfs_solver = BFS(maze)

t_start = time.time()
bfs_path, bfs_nodes = bfs_solver.solve(start, goal)
bfs_time = (time.time() - t_start) * 1000

print(f"BFS: length={len(bfs_path)}, explored={bfs_nodes}, time={bfs_time:.2f} ms")
if bfs_path:
    print("BFS Path:")
    maze.print_maze(bfs_path)
else:
    print("BFS: No path found")

print("-" * 30)

# ----------------- DFS Section -----------------
dfs_solver = DFS(maze)

t_start = time.time()
dfs_path, dfs_nodes = dfs_solver.solve(start, goal)
dfs_time = (time.time() - t_start) * 1000

print(f"DFS: length={len(dfs_path)}, explored={dfs_nodes}, time={dfs_time:.2f} ms")
if dfs_path:
    print("DFS Path:")
    maze.print_maze(dfs_path)
else:
    print("DFS: No path found")

print("-" * 30)

# ----------------- A* Section -----------------
astar_solver = AStarSearch(maze)

t_start = time.time()
astar_path, astar_nodes = astar_solver.solve(start, goal)
astar_time = (time.time() - t_start) * 1000

print(f"A*:  length={len(astar_path)}, explored={astar_nodes}, time={astar_time:.2f} ms")
if astar_path:
    print("A* Path:")
    maze.print_maze(astar_path)
else:
    print("A*: No path found")
    
# ----------------- UCS Section -----------------
ucs_solver = UCS(maze)

t_start = time.time()
ucs_path, ucs_nodes = ucs_solver.solve(start, goal)
ucs_time = (time.time() - t_start) * 1000


print(f"UCS: length={len(ucs_path)}, explored={ucs_nodes}, time={ucs_time:.2f} ms")

if ucs_path:
    print("UCS Path:")
    maze.print_maze(ucs_path)
else:
    print("UCS: No path found")
    
# ----------------- IDS Section -----------------
ids_solver = IDS(maze)

t_start = time.time()
ids_path, ids_nodes = ids_solver.solve(start, goal)
ids_time = (time.time() - t_start) * 1000

print(f"IDS: length={len(ids_path)}, explored={ids_nodes}, time={ids_time:.2f} ms")
if ids_path:
    print("IDS Path:")
    maze.print_maze(ids_path)
else:
    print("IDS: No path found")
    
# ----------------- Hill Climbing Section -----------------
hc_solver = HillClimbing(maze)

t_start = time.time()
hc_path, hc_nodes = hc_solver.solve(start, goal)
hc_time = (time.time() - t_start) * 1000

print(f"Hill Climbing: length={len(hc_path)}, explored={hc_nodes}, time={hc_time:.2f} ms")
if hc_path:
    print("Hill Climbing Path:")
    maze.print_maze(hc_path)
else:
    print("Hill Climbing: Stuck in local maximum (No path found)")
    
# ----------------- Genetic Algorithm Section -----------------
# You can adjust population_size and generations to improve accuracy
ga_solver = GeneticAlgorithm(maze, population_size=100, generations=200)

t_start = time.time()
ga_path, ga_nodes = ga_solver.solve(start, goal)
ga_time = (time.time() - t_start) * 1000

print(f"Genetic Algorithm: length={len(ga_path)}, explored={ga_nodes}, time={ga_time:.2f} ms")

# Check if path exists AND if it actually reached the goal
if ga_path and ga_path[-1] == goal:
    print("Genetic Algorithm Path:")
    maze.print_maze(ga_path)
else:
    print("Genetic Algorithm: Goal not reached (Max generations exceeded or stuck)")
    

# ----------------- Greedy Best-First Search Section -----------------
greedy_solver = GreedyBFS(maze)

t_start = time.time()
greedy_path, greedy_nodes = greedy_solver.solve(start, goal)
greedy_time = (time.time() - t_start) * 1000

print(f"Greedy BFS: length={len(greedy_path)}, explored={greedy_nodes}, time={greedy_time:.2f} ms")

if greedy_path:
    print("Greedy BFS Path:")
    maze.print_maze(greedy_path)
else:
    print("Greedy BFS: No path found")