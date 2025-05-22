import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def plot_world(grid, ant, step_number, show_scent=True):
    size = grid.size
    display_grid = np.zeros((size, size, 3))  # RGB

    # Base layer: food scent as green
    if show_scent:
        norm_scent = grid.food_scent / (np.max(grid.food_scent) + 1e-5)
        display_grid[:, :, 1] = norm_scent * 0.3  # Greenish background

    # Pheromone heatmap overlay: blue
    norm_pheromones = grid.food_path / (np.max(grid.food_path) + 1e-5)
    display_grid[:, :, 2] += norm_pheromones * 0.8  # Blue

    # Obstacles: black
    for x, y in grid.obstacle_positions:
        display_grid[x, y] = [0, 0, 0]

    # Food: red
    for x, y in grid.food_positions:
        display_grid[x, y] = [1, 0, 0]

    # Colony: yellow
    cx, cy = grid.colony_position
    display_grid[cx, cy] = [1, 1, 0]

    # Ant position: white
    ax, ay = ant.pos
    display_grid[ax, ay] = [1, 1, 1]

    plt.imshow(display_grid, interpolation="nearest")
    plt.title("Ant Colony Simulation")
    plt.axis("off")
    plt.savefig(f"images/ant_colony-{step_number}.png")
