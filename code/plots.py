import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_world(grid, ants, step_number, show_scent=True):
    size = grid.size
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.set_title(f"Ant Simulation - Step {step_number}")

    # Heatmaps (with extent to match grid)
    if show_scent:
        ax.imshow(grid.food_scent, cmap='Reds', alpha=0.2, origin='upper', extent=(0, size, 0, size))
    ax.imshow(grid.food_path, cmap='Blues', alpha=0.4, origin='upper', extent=(0, size, 0, size))

    # Obstacles
    for x, y in grid.obstacle_positions:
        rect = patches.Rectangle((y, size - x - 1), 1, 1, linewidth=1, edgecolor='black', facecolor='gray', zorder=1)
        ax.add_patch(rect)

    # Food using 🍎 emoji
    emoji_size = max(6, int(300 / size))
    for x, y in grid.food_positions:
        ax.text(
            y + 0.5,
            size - x - 0.5,
            "🍎",
            fontsize=emoji_size,
            ha='center', va='center',
            fontname="Segoe UI Emoji",
            zorder=5
        )

    # Colony using 🏠 emoji
    cx, cy = grid.colony_position
    ax.text(
        cy + 0.5,
        size - cx - 0.5,
        "🏠",
        fontsize=emoji_size,
        ha='center', va='center',
        fontname="Segoe UI Emoji",
        zorder=5
    )

    for ant in ants:
        # Ant using 🐜 emoji
        ax.text(
            ant.pos[1] + 0.5,
            size - ant.pos[0] - 0.5,
            "🐜",
            fontsize=emoji_size,
            ha='center', va='center',
            fontname="Segoe UI Emoji",
            zorder=10
        )

    plt.savefig(f"images/ant_colony-{step_number:03}.png")
    plt.close()
