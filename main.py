#!/usr/bin/env python
import numpy as np
import random
import os
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy.typing import NDArray

import code.grid as grid
import code.ants as ants
import code.plots as plots
from code.parse_config import parse_config

# Load config
config = parse_config("config.json")
environment_path = config["environment_path"]

# Load environment
with open(environment_path, "r") as f:
    data = json.load(f)

grid_size = data["size"]
start_food_amount = config["colony_start_amount"]
extension = config["extension"]
elitist_ant_count = config["elitist_ant_count"]
pheromone_constant = config["pheromone_constant"]

# Set simulation parameters
seed = config["seed"]
cycles = config["cycles"]

# Initialize
random.seed(seed)
np.random.seed(seed)
mode = config["mode"]

food_amount_amounts = []
ants_efficiency_efficiencies = []
success_trip_rate_rate = []
visited_amounts = []

seeds = [random.randint(1, 10000) for _ in range(cycles)]
for cycle, seed in enumerate(seeds):
    environment = grid.Grid(
        size=grid_size,
        extension=extension,
        start_food_amount=start_food_amount,
        elitist_ant_count=elitist_ant_count,
        pheromone_constant=pheromone_constant,
    )
    environment.place_colony(tuple(data["colony"]))
    for food in data["food"]:
        environment.add_food(tuple(food))
    for obstacle in data["obstacles"]:
        environment.add_obstacle(tuple(obstacle))

    environment.real_shortest_paths = environment.compute_shortest_paths()

    random.seed(seed)
    np.random.seed(seed)

    ant_list = [
        ants.Ant(
            environment,
            max_energy=config["ant_energy"],
            max_carry_amount=config["ant_carry_amount"],
            exploration_desire=config["exploration_desire"],
            mode=mode,
        )
        for _ in range(config["num_ants"])
    ]

    food_amounts = []
    visited_area = []
    ants_efficiency = []
    success_trip_rate = []
    avg_food_trip_length = []
    total_energy_consumed = 0
    avg_food_trip_length = []
    all_successful_paths = []

    output_path = f"images/{cycle}/ant_animation.mp4"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if "animation" in config["observables"]:
        fig, ax = plt.subplots()

        def update(frame):
            global total_energy_consumed
            ax.clear()
            food_amounts.append(environment.colony_food)

            total_successful_trips = 0
            total_completed_trips = 0
            sum_latest_food_trip_length = 0
            if frame == 0:
                plots.draw_world(ax, environment, ant_list, step_number=0)
            else:
                environment.evaporate_pheromones()
                for ant in ant_list:
                    ant.next_step(frame)
                    if not ant.dead:
                        total_energy_consumed += 1
                    total_successful_trips += ant.success_trip
                    total_completed_trips += ant.completed_trip
                    sum_latest_food_trip_length += ant.last_food_trip_length
                avg_food_trip_length.append(sum_latest_food_trip_length / len(ant_list))

                if extension == "elitist":
                    environment.reinforce_best_path()

                visited_area.append(np.count_nonzero(environment.visited))

                plots.draw_world(ax, environment, ant_list, frame)

            if "ant_efficiency" in config["observables"]:
                total_collected = (
                    len(environment.food_at_nest_instances) * config["ant_carry_amount"]
                )

                efficiency = total_collected / (total_energy_consumed + 1e-3)
                ants_efficiency.append(round(efficiency, 2))

            if "success_trips_rate" in config["observables"]:
                if total_completed_trips == 0:
                    success_trip_rate.append(np.nan)
                else:
                    success_trip_rate.append(
                        total_successful_trips / total_completed_trips
                    )

        for ant in ant_list:
            all_successful_paths.append(ant.all_successful_paths)

        # Animate
        ani = animation.FuncAnimation(
            fig, update, frames=config["frames"], interval=config["frame_interval"]
        )

        # Save video
        ani.save(output_path, writer="ffmpeg")

    else:
        for step in range(config["frames"]):
            food_amounts.append(environment.colony_food)

            total_successful_trips = 0
            total_completed_trips = 0
            sum_latest_food_trip_length = 0
            environment.evaporate_pheromones()
            for ant in ant_list:
                ant.next_step(step)
                if not ant.dead:
                    total_energy_consumed += 1
                total_successful_trips += ant.success_trip
                total_completed_trips += ant.completed_trip
                sum_latest_food_trip_length += ant.last_food_trip_length
            avg_food_trip_length.append(sum_latest_food_trip_length / len(ant_list))

            if extension == "elitist":
                environment.reinforce_best_path()

            if "ant_efficiency" in config["observables"]:
                total_collected = (
                    len(environment.food_at_nest_instances) * config["ant_carry_amount"]
                )

                efficiency = total_collected / (total_energy_consumed + 1e-3)
                ants_efficiency.append(round(efficiency, 2))

            if "success_trips_rate" in config["observables"]:
                if total_completed_trips == 0:
                    success_trip_rate.append(np.nan)
                else:
                    success_trip_rate.append(
                        total_successful_trips / total_completed_trips
                    )

            visited_area.append(np.count_nonzero(environment.visited))

        for ant in ant_list:
            all_successful_paths.append(ant.all_successful_paths)

    # Plotted Output
    if "colony_food" in config["observables"]:
        plots.colony_food(food_amounts, cycle)

    if "ant_efficiency" in config["observables"]:
        plots.ant_efficiency(ants_efficiency, cycle)

    if "success_trips_rate" in config["observables"]:
        plots.ant_trip_success_rate(success_trip_rate, cycle)

    if "visited_area" in config["observables"]:
        plots.visited_area(visited_area, cycle)

    if "avg_latest_success_trip" in config["observables"]:
        plots.average_steps_per_ant(avg_food_trip_length, cycle)

    if "plot_paths" in config["observables"]:
        plots.plot_paths_on_grid(environment, all_successful_paths, cycle)

    # Printed Output
    if "time_to_first_path" in config["observables"]:
        if environment.food_at_nest_instances:
            time_to_first_path = min(s for _, s in environment.food_at_nest_instances)
        else:
            time_to_first_path = None
        print("Time to First Path:", time_to_first_path)

    if "time_to_shortest_path" in config["observables"]:
        print("Time to Shortest Path:", environment.best_path_found_step)

    if "ant_shortest_path_len" in config["observables"]:
        print(f"Shortest Path Length found by Ants: {environment.best_path_length - 1}")

    print("=========================")

    food_amount_amounts.append(food_amounts)
    ants_efficiency_efficiencies.append(ants_efficiency)
    success_trip_rate_rate.append(success_trip_rate)
    visited_amounts.append(visited_area)

for i, path in enumerate(environment.real_shortest_paths):
    print(f"Real Shortest Path Length to Food: {len(path) - 1}")

food_amount_tot = np.array(food_amount_amounts)
ants_efficiency_tot = np.array(ants_efficiency_efficiencies)
success_trip_rate_tot = np.array(success_trip_rate_rate)
visited_amount_tot = np.array(visited_amounts)

food_amount_avg = np.average(food_amount_tot, axis=0)
ants_efficiency_avg = np.average(ants_efficiency_tot, axis=0)
success_trip_rate_avg = np.average(success_trip_rate_tot, axis=0)
visited_amount_avg = np.average(visited_amount_tot, axis=0)

food_amount_std = np.std(food_amount_tot, axis=0, mean=food_amount_avg)
ants_efficiency_std = np.std(ants_efficiency_tot, axis=0, mean=ants_efficiency_avg)
success_trip_rate_std = np.std(
    success_trip_rate_tot, axis=0, mean=success_trip_rate_avg
)
visited_amount_std = np.std(visited_amount_tot, axis=0, mean=visited_amount_avg)

x = np.arange(config["frames"])  # x-axis points

# Colony Food plot
plt.figure(figsize=(8, 5))
plt.plot(x, food_amount_avg, label="Colony Food Avg", color="blue")
plt.fill_between(
    x,
    food_amount_avg - food_amount_std,
    food_amount_avg + food_amount_std,
    color="blue",
    alpha=0.3,
    label="Std Dev",
)
plt.title("Food Available at Colony: Avg Over Cycles")
plt.xlabel("Step")
plt.ylabel("Food at Colony")
plt.legend()
plt.savefig("images/global_colony_food.png")
plt.close()

# Ant Efficiency plot
plt.figure(figsize=(8, 5))
plt.plot(x, ants_efficiency_avg, label="Ant Efficiency Avg", color="green")
plt.fill_between(
    x,
    ants_efficiency_avg - ants_efficiency_std,
    ants_efficiency_avg + ants_efficiency_std,
    color="green",
    alpha=0.3,
    label="Std Dev",
)
plt.title("Ant Efficiency: Avg Over Cycles")
plt.xlabel("Step")
plt.ylabel("Collected Food / Consumed Energy")
plt.legend()
plt.savefig("images/global_ant_efficiency.png")
plt.close()

# Success Trip Rate plot
plt.figure(figsize=(8, 5))
plt.plot(x, success_trip_rate_avg, label="Success Trip Rate Avg", color="red")
plt.fill_between(
    x,
    success_trip_rate_avg - success_trip_rate_std,
    success_trip_rate_avg + success_trip_rate_std,
    color="red",
    alpha=0.3,
    label="Std Dev",
)
plt.title("Rate of Successful Trips: Avg Over Cycles")
plt.xlabel("Step")
plt.ylabel("Successful Trips / Total Completed Trips")
plt.legend()
plt.savefig("images/global_success_trips_rate.png")
plt.close()

# Visited Amount plot
plt.figure(figsize=(8, 5))
plt.plot(x, visited_amount_avg, label="Visited Amount Avg", color="purple")
plt.fill_between(
    x,
    visited_amount_avg - visited_amount_std,
    visited_amount_avg + visited_amount_std,
    color="purple",
    alpha=0.3,
    label="Std Dev",
)
plt.title("Area explored by the colony: Avg Over Cycles")
plt.xlabel("Step")
plt.ylabel("Visited Area")
plt.legend()
plt.savefig("images/global_visited_area.png")
plt.close()

print("Plots saved to the 'images/' folder.")
