import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np



def draw_world(ax, grid, ants, step_number, show_scent=True):
    ax.clear()
    size = grid.size
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_title(f"Ant Simulation - Step {step_number}")

    if show_scent:
        ax.imshow(grid.food_scent, cmap="Greens", alpha=0.2,
                  origin="upper", extent=(0, size, 0, size))
    ax.imshow(grid.food_path, cmap="Blues", alpha=0.4,
              origin="upper", extent=(0, size, 0, size))

    for x, y in grid.obstacle_positions:
        rect = patches.Rectangle(
            (y, size - x - 1), 1, 1, linewidth=1, edgecolor="black", facecolor="black", zorder=1)
        ax.add_patch(rect)

    for x, y in grid.food_positions:
        rect = patches.Rectangle(
            (y, size - x - 1), 1, 1, linewidth=1, edgecolor="black", facecolor="green", zorder=5)
        ax.add_patch(rect)
        ax.text(y + 0.5, size - x - 0.5, "Food", fontsize=8, ha="center",
                va="center", weight="bold", color="white", zorder=6)

    if grid.colony_position is not None:
        cx, cy = grid.colony_position
        rect = patches.Rectangle(
            (cy, size - cx - 1), 1, 1, linewidth=1, edgecolor="black", facecolor="orange", zorder=5)
        ax.add_patch(rect)
        ax.text(cy + 0.5, size - cx - 0.5, "Home", fontsize=8, ha="center",
                va="center", weight="bold", color="white", zorder=6)

    # Red dots for ants with jitter for overlaps
    pos_dict = {}
    for ant in ants:
        pos = ant.pos
        if pos not in pos_dict:
            pos_dict[pos] = []
        pos_dict[pos].append(ant)

    for (x, y), ant_group in pos_dict.items():
        for idx, ant in enumerate(ant_group):
            jitter_x = (idx % 3 - 1) * 0.1
            jitter_y = (idx // 3 - 1) * 0.1
            ax.plot(y + 0.5 + jitter_x, size - x - 0.5 +
                    jitter_y, "ro", markersize=5, zorder=10)
