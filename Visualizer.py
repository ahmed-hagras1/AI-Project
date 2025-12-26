import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import numpy as np
import time
import os

# Import your existing classes
from Maze import Maze
from BFS import BFS
from DFS import DFS
from AStarSearch import AStarSearch
from IDS import IDS
from HillClimbing import HillClimbing
from GeneticAlgorithm import GeneticAlgorithm
from GreedyBFS import GreedyBFS
from UCS import UCS

def get_visualization_grid(maze_obj, path=None):
    """
    Converts the maze grid into a color map for matplotlib.
    """
    grid = np.array(maze_obj.grid)
    vis_grid = np.zeros_like(grid)
    
    # Map: Wall=1, Path=0
    # For visualization: 0=White(Path), 1=Black(Wall)
    vis_grid[grid == 1] = 1 
    vis_grid[grid == 0] = 0

    if path:
        for (r, c) in path:
            if 0 <= r < maze_obj.n and 0 <= c < maze_obj.n:
                vis_grid[r][c] = 2 # Path color

    # Mark Start and Goal
    start = (0, 0)
    goal = (maze_obj.n - 1, maze_obj.n - 1)
    vis_grid[start] = 3
    vis_grid[goal] = 4

    return vis_grid

def plot_static_comparison(maze, results):
    """
    Plots a grid of subplots showing the solution for each algorithm.
    """
    num_algos = len(results)
    cols = 4
    rows = (num_algos + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
    fig.suptitle(f"Algorithm Comparison (Maze Size: {maze.n}x{maze.n})", fontsize=16)
    
    # Custom colormap: [Path, Wall, PathTrace, Start, Goal]
    # Colors: White, Black, Blue, Green, Red
    cmap = mcolors.ListedColormap(['white', 'black', 'deepskyblue', 'lime', 'red'])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    axes_flat = axes.flatten() if num_algos > 1 else [axes]

    for i, (name, result) in enumerate(results.items()):
        path, nodes, exec_time = result
        ax = axes_flat[i]
        
        vis_grid = get_visualization_grid(maze, path)
        
        ax.imshow(vis_grid, cmap=cmap, norm=norm)
        
        # Title with stats
        status = "Solved" if path else "Failed"
        if name == "Hill Climbing" and not path: status = "Stuck"
        
        title_text = f"{name}\n{status}\nLen: {len(path)} | Exp: {nodes}"
        ax.set_title(title_text, fontsize=10)
        ax.axis('off')

    # Hide empty subplots
    for j in range(i + 1, len(axes_flat)):
        axes_flat[j].axis('off')

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.savefig("Images/All_Algorithms_Solved.png")
    print("Static comparison saved to 'Images/All_Algorithms_Solved.png'")
    # plt.show() 

def create_combined_animation(maze, results, algorithm_order):
    """
    Creates a SINGLE video file that plays all algorithms sequentially.
    """
    print("Generating combined animation timeline...")
    
    # 1. Build the timeline of frames
    # timeline is a list of dictionaries, where each dict is one frame of the video
    timeline = []
    
    for name in algorithm_order:
        # Check if this algorithm was run and found a valid path
        if name in results and results[name][0]: 
            path = results[name][0]
            
            # Add running frames (agent moving)
            for i in range(len(path)):
                timeline.append({
                    "algo": name,
                    "path_slice": path[:i+1], # Path up to current step
                    "current_pos": path[i]
                })
            
            # Add PAUSE frames at the end of each algorithm (so viewer can see the result)
            # 15 frames pause * 60ms interval ~= 1 second pause
            for _ in range(15): 
                timeline.append({
                    "algo": name,
                    "path_slice": path,
                    "current_pos": path[-1]
                })

    if not timeline:
        print("No paths found to animate.")
        return

    # 2. Setup the Plot
    fig, ax = plt.subplots(figsize=(7, 7))
    
    # Static Background (Walls and Empty Space)
    grid = np.array(maze.grid)
    cmap = mcolors.ListedColormap(['white', 'black'])
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=1)
    
    # Dynamic Elements (Agent, Trail, Title)
    agent, = ax.plot([], [], 'ro', markersize=12, label='Agent', zorder=5) # Red dot
    trail, = ax.plot([], [], 'b.', markersize=6, alpha=0.5, zorder=3) # Blue dots
    
    # Title Text object (we update this every frame)
    title_text = ax.text(0.5, 1.02, "", transform=ax.transAxes, ha="center", fontsize=14, fontweight='bold', color='darkblue')

    # Goal Marker
    ax.plot(maze.n-1, maze.n-1, 'rx', markersize=12, markeredgewidth=3)
    ax.text(maze.n-1, maze.n-1, ' GOAL', color='red', fontsize=12)
    ax.axis('off')

    def init():
        agent.set_data([], [])
        trail.set_data([], [])
        title_text.set_text("")
        return agent, trail, title_text

    def update(frame_idx):
        frame_data = timeline[frame_idx]
        
        # Update Title
        title_text.set_text(f"Algorithm: {frame_data['algo']}")
        
        # Update Agent Position
        # Note: matplotlib plots (x, y), but matrix is [row][col]. So we plot (col, row).
        r, c = frame_data['current_pos']
        agent.set_data([c], [r])
        
        # Update Trail
        path = frame_data['path_slice']
        if path:
            rs, cs = zip(*path)
            trail.set_data(cs, rs)
            
        return agent, trail, title_text

    print(f"Rendering {len(timeline)} frames... This may take a moment.")
    
    # Interval=60ms means ~16 FPS. 
    ani = animation.FuncAnimation(fig, update, frames=len(timeline), init_func=init, blit=True, interval=60)
    
    filename = "Images/Combined_Algorithms.gif"
    ani.save(filename, writer='pillow', fps=15)
    print(f"Combined animation saved to '{filename}'")
    plt.close()

def main():
    # 1. Setup Maze
    maze_size = 15
    print(f"Generating {maze_size}x{maze_size} Maze...")
    maze = Maze(maze_size, wall_prob=0.3)
    
    # 2. Define Algorithms to run (Order matters for the video!)
    algorithms_list = [
        ("BFS", BFS(maze)),
        ("DFS", DFS(maze)),
        ("UCS", UCS(maze)),
        ("A* (Manhattan)", AStarSearch(maze, heuristic_type="manhattan")),
        ("IDS", IDS(maze)),
        ("Greedy BFS", GreedyBFS(maze)),
        ("Hill Climbing", HillClimbing(maze)),
        ("Genetic Algo", GeneticAlgorithm(maze, population_size=100, generations=200)),
    ]
    
    results = {}
    algo_names_order = [] # To keep track of order for the video

    # 3. Run Solvers
    start_node = (0, 0)
    goal_node = (maze.n - 1, maze.n - 1)

    for name, solver in algorithms_list:
        algo_names_order.append(name)
        print(f"Running {name}...")
        t0 = time.time()
        path, nodes = solver.solve(start_node, goal_node)
        t1 = time.time()
        results[name] = (path, nodes, t1-t0)

    # 4. Generate Static Comparison Image
    plot_static_comparison(maze, results)

    # 5. Generate ONE Combined Animation
    create_combined_animation(maze, results, algo_names_order)

if __name__ == "__main__":
    if not os.path.exists("Images"):
        os.makedirs("Images")
    main()