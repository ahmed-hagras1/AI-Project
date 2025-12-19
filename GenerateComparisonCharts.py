import matplotlib.pyplot as plt
import numpy as np

# Data
algorithms = ['BFS', 'DFS', 'A* (Man)', 'UCS', 'IDS', 'Hill Climb', 'Genetic', 'Greedy']
time_data = [0.08, 0.04, 0.15, 0.11, 0.52, 0.04, 129.26, 0.06]
nodes_data = [46, 29, 31, 48, 407, 20, 11600, 23]
path_data = [19, 21, 19, 19, 19, 21, 19, 19]

# Colors for bars
colors = ['#3498db', '#9b59b6', '#2ecc71', '#1abc9c', '#f1c40f', '#e67e22', '#e74c3c', '#34495e']

def save_chart(data, title, ylabel, filename, log_scale=False):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, data, color=colors)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}',
                ha='center', va='bottom')

    if log_scale:
        plt.yscale('log')
        plt.ylabel(f"{ylabel} (Log Scale)")

    plt.tight_layout()
    plt.savefig(f"Images/{filename}") # Saves to Images folder
    plt.close()

# 1. Path Length Comparison
save_chart(path_data, 'Path Length Comparison (Lower is Better)', 'Steps', 'compare_path.png')

# 2. Nodes Explored (Log Scale due to Genetic Algo)
save_chart(nodes_data, 'Nodes Explored Comparison (Efficiency)', 'Nodes Count', 'compare_nodes.png', log_scale=True)

# 3. Time Comparison (Log Scale due to Genetic Algo)
save_chart(time_data, 'Execution Time Comparison (Speed)', 'Time (ms)', 'compare_time.png', log_scale=True)

print("Charts generated successfully in the 'Images/' folder!")