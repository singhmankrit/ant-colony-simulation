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


def colony_food(food_gathered):
    stps = np.arange(len(food_gathered))
    fig = plt.figure()
    plt.plot(
        stps[1:],
        food_gathered[1:],
        label="colony food",
    )
    plt.legend()
    plt.xlabel("Step")
    plt.ylabel("Food at Colony")
    plt.title("Food Available at Colony Over Time")
    fig.savefig("images/colony_food.png")


def ant_efficiency(ants_efficiency):
    stps = np.arange(len(ants_efficiency))
    fig = plt.figure()
    plt.plot(
        stps[1:],
        ants_efficiency[1:],
        label="ant efficiency",
    )
    plt.legend()
    plt.xlabel("Step")
    plt.ylabel("Collected Food / Consumed Energy")
    plt.title("Total Ant Efficiency Over Time")
    fig.savefig("images/ant_efficiency.png")


def ant_trip_success_rate(success_trip_rate):
    stps = np.arange(len(success_trip_rate))
    fig = plt.figure()
    plt.plot(
        stps[1:],
        success_trip_rate[1:],
        label="rate of successful trips",
    )
    plt.legend()
    plt.xlabel("Step")
    plt.ylabel("Successful Trips / Total Completed Trips")
    plt.title("Rate of Successful Trips Over Time")
    fig.savefig("images/success_trips.png")


def average_steps_per_ant(average_steps_per_ant):
    stps = np.arange(len(average_steps_per_ant))
    fig = plt.figure()
    plt.plot(
        stps[1:],
        average_steps_per_ant[1:],
        label="average food trip length per ant",
    )
    plt.legend()
    plt.xlabel("Step")
    plt.ylabel("Length of Latest Successful Trips / Total Ants")
    plt.title("Average Length of Successful Trips Over Time")
    fig.savefig("images/average_length_of_food_trips.png")


def plot_paths_on_grid(environment):
    # --- Plot ---
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, environment.size)
    ax.set_ylim(0, environment.size)
    ax.set_xticks(range(environment.size + 1))
    ax.set_yticks(range(environment.size + 1))
    ax.set_aspect("equal")
    ax.grid(True)

    # Color grid
    for x in range(environment.size):
        for y in range(environment.size):
            val = environment.grid[x, y]
            if val == 1:
                color = "red"  # Colony
            elif val == 2:
                color = "green"  # Food
            elif val == 3:
                color = "black"  # Obstacle
            else:
                continue
            rect = patches.Rectangle((x, y), 1, 1, facecolor=color, edgecolor="black")
            ax.add_patch(rect)

    # Plot paths as arrows or lines
    for i, path in enumerate(environment.real_shortest_paths):
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            ax.arrow(
                x1 + 0.5,
                y1 + 0.5,
                (x2 - x1) * 0.8,
                (y2 - y1) * 0.8,
                head_width=0.2,
                length_includes_head=True,
                color="blue",
                alpha=0.6,
            )
            xs, ys = zip(*path)
            ax.text(xs[-1] + 0.1, ys[-1], f"L={len(path) -1}", fontsize=9, color="blue")
        # Label path
        if path:
            x0, y0 = path[-1]
            ax.text(x0 + 0.5, y0 + 0.5, f"{i}", color="blue", ha="center", va="center")

    plt.title("Shortest Paths from Colony to Food")
    plt.savefig("images/shortest_paths.png", dpi=300)
