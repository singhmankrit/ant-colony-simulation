import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from . import grid


def draw_world(ax, grid, ants, step_number):
    ax.clear()
    size = grid.size
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_title(f"Ant Simulation - Step {step_number}")

    ax.imshow(
        np.average(grid.food_path[::-1, :], axis=-1),
        cmap="Blues",
        alpha=0.4,
        origin="upper",
        extent=(0, size, 0, size),
    )
    x, y = np.meshgrid(np.arange(size), np.arange(size))
    ax.quiver(x + 0.5, y + 0.5, grid.food_path[:, :, 1], 0, scale=2)
    ax.quiver(x + 0.5, y + 0.5, -grid.food_path[:, :, 3], 0, scale=2)
    ax.quiver(x + 0.5, y + 0.5, 0, grid.food_path[:, :, 0], scale=2)
    ax.quiver(x + 0.5, y + 0.5, 0, -grid.food_path[:, :, 2], scale=2)

    for x, y in grid.obstacle_positions:
        rect = patches.Rectangle(
            (x, y),
            1,
            1,
            linewidth=1,
            edgecolor="black",
            facecolor="black",
            zorder=1,
        )
        ax.add_patch(rect)

    for x, y in grid.food_positions:
        rect = patches.Rectangle(
            (x, y),
            1,
            1,
            linewidth=1,
            edgecolor="black",
            facecolor="green",
            zorder=5,
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.5,
            y + 0.5,
            "Food",
            fontsize=8,
            ha="center",
            va="center",
            weight="bold",
            color="white",
            zorder=6,
        )

    if grid.colony_position is not None:
        cx, cy = grid.colony_position
        rect = patches.Rectangle(
            (cx, cy),
            1,
            1,
            linewidth=1,
            edgecolor="black",
            facecolor="orange",
            zorder=5,
        )
        ax.add_patch(rect)
        ax.text(
            cx + 0.5,
            cy + 0.5,
            "Home",
            fontsize=8,
            ha="center",
            va="center",
            weight="bold",
            color="white",
            zorder=6,
        )

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
            ax.plot(
                x + 0.5 + jitter_x,
                y + 0.5 + jitter_y,
                "ro",
                markersize=5,
                zorder=10,
            )

    # Position top-left corner (some padding from edge)
    padding = 0.3
    ax.text(
        padding,
        size - padding,
        f"Ants alive: {len([ant for ant in ants if not ant.dead])}",
        fontsize=10,
        color="red",
        weight="bold",
        ha="left",
        va="top",
        zorder=20,
        bbox=dict(
            facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.3"
        ),
    )
    ax.text(
        size - padding,
        size - padding,
        f"Food at colony: {grid.colony_food}",
        fontsize=10,
        color="green",
        weight="bold",
        ha="right",
        va="top",
        zorder=20,
        bbox=dict(
            facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.3"
        ),
    )


def hist_distances(grid, steps):
    gathered = np.array([y for x, y in grid.food_gathered_instances])
    back = np.array([y for x, y in grid.food_at_nest_instances])

    cum_gathered = np.zeros(steps)
    cum_back = np.zeros(steps)
    stps = np.arange(steps)

    for step in gathered:
        cum_gathered[step:] += 1

    for step in back:
        cum_back[step:] += 1

    fig = plt.figure()
    plt.plot(
        stps,
        cum_gathered,
        label="total gathered food",
    )
    plt.plot(
        stps,
        cum_back,
        label="food brought to the colony",
    )
    plt.legend()
    plt.xlabel("step")
    plt.ylabel("gathered food")
    plt.title("Total food gathered")
    fig.savefig("images/total_gathered_food.png")

    fig = plt.figure()
    plt.plot(
        stps[1:],
        cum_gathered[1:] / stps[1:],
        label="gathered food/step",
    )
    plt.plot(
        stps[1:],
        cum_back[1:] / stps[1:],
        label="food brought to the colony/step",
    )
    plt.legend()
    plt.xlabel("step")
    plt.ylabel("gathered food / step")
    plt.title("Average food gathered per step")
    fig.savefig("images/average_gathered_food.png")
