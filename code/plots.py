import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize, ListedColormap
import matplotlib.cm as cm


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


def colony_food(food_gathered, cycle):
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
    fig.savefig(f"images/{cycle}/colony_food.png")
    plt.close()


def ant_efficiency(ants_efficiency, cycle):
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
    fig.savefig(f"images/{cycle}/ant_efficiency.png")
    plt.close()


def visited_area(areas, cycle):
    stps = np.arange(len(areas))
    fig = plt.figure()
    plt.plot(
        stps,
        areas,
        label="visited area",
    )
    plt.legend()
    plt.xlabel("Step")
    plt.ylabel("Visited Area")
    plt.title("Area explored by the colony")
    fig.savefig(f"images/{cycle}/visited_area.png")
    plt.close()


def ant_trip_success_rate(success_trip_rate, cycle):
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
    fig.savefig(f"images/{cycle}/success_trips.png")
    plt.close()


def average_steps_per_ant(average_steps_per_ant, cycle):
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
    fig.savefig(f"images/{cycle}/average_length_of_food_trips.png")
    plt.close()


def plot_paths_on_grid(environment, all_successful_paths, cycle):
    # --- Compute visitation heatmap ---
    visit_counts = np.zeros((environment.size, environment.size), dtype=int)
    for ant_paths in all_successful_paths:
        for path in ant_paths:
            for x, y in path:
                visit_counts[x, y] += 1

    max_count = np.max(visit_counts)
    norm = Normalize(vmin=0, vmax=max_count if max_count > 0 else 1)

    # --- Transparent light yellow colormap ---
    light_yellow_cmap = cm.get_cmap("Wistia", 256)
    colors = light_yellow_cmap(np.linspace(0, 1, 256))
    colors[:, -1] = np.linspace(0, 0.4, 256)  # transparency from 0 to 0.4
    transparent_yellow_cmap = ListedColormap(colors)

    # --- Plotting setup ---
    _, ax = plt.subplots(figsize=(6, 7))
    ax.set_xlim(0, environment.size)
    ax.set_ylim(0, environment.size)
    ax.set_xticks(range(environment.size + 1))
    ax.set_yticks(range(environment.size + 1))
    ax.set_aspect("equal")
    ax.grid(color="gray", alpha=0.3)

    # --- Draw environment grid with visit shading ---
    for x in range(environment.size):
        for y in range(environment.size):
            val = environment.grid[x, y]

            visit_value = (
                transparent_yellow_cmap(norm(visit_counts[x, y]))
                if visit_counts[x, y] > 0
                else "white"
            )

            if val == 1:
                face_color = "red"  # Colony
            elif val == 2:
                face_color = "green"  # Food
            elif val == 3:
                face_color = "black"  # Obstacle
            else:
                face_color = visit_value

            rect = patches.Rectangle(
                (x, y), 1, 1, facecolor=face_color, edgecolor="black"
            )
            ax.add_patch(rect)

    # --- Plot real shortest paths in blue ---
    real_length = None
    for i, path in enumerate(environment.real_shortest_paths):
        if not path:
            continue
        real_length = len(path) - 1
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            ax.arrow(
                x1 + 0.5,
                y1 + 0.5,
                (x2 - x1) * 0.8,
                (y2 - y1) * 0.8,
                head_width=0.2,
                length_includes_head=True,
                color="blue",
                alpha=0.8,
            )

    # --- Plot ant's best path in red ---
    ant_best_path = environment.best_path
    ant_length = None
    if ant_best_path:
        ant_length = len(ant_best_path) - 1
        for (x1, y1), (x2, y2) in zip(ant_best_path, ant_best_path[1:]):
            ax.arrow(
                x1 + 0.5,
                y1 + 0.5,
                (x2 - x1) * 0.8,
                (y2 - y1) * 0.8,
                head_width=0.2,
                length_includes_head=True,
                color="red",
                alpha=0.8,
            )
        x0, y0 = ant_best_path[-1]
        ax.text(x0 + 0.5, y0 + 0.5, f"{i}", color="red", ha="center", va="center")

    # --- Add bottom legend ---
    legend_elements = []

    if real_length is not None:
        legend_elements.append(
            Line2D(
                [0], [0], color="blue", lw=2, label=f"Shortest Path (L={real_length})"
            )
        )
    if ant_length is not None:
        legend_elements.append(
            Line2D([0], [0], color="red", lw=2, label=f"Ant Path (L={ant_length})")
        )

    legend_elements.append(
        Patch(
            facecolor=cm.Wistia(0.7),
            edgecolor="black",
            label="Visit Frequency for Successful Trips",
        )
    )

    ax.legend(
        handles=legend_elements,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=2,
        frameon=False,
        fontsize=10,
    )

    plt.title("Paths from Colony to Food")
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig(f"images/{cycle}/shortest_paths.png", dpi=300, bbox_inches="tight")
    plt.close()
