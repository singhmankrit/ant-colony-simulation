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
time_to_firsts = []
time_to_shortests = []
shortest_ant_paths = []
populations = []
all_successful_paths_ever = []
avg_food_trip_lengths = []

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
    total_energy_consumed = 0
    avg_food_trip_length = []
    all_successful_paths = []
    ant_population = []
    ants_dead_at_step = -1

    output_path = f"images/{cycle}/ant_animation.mp4"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if "animation" in config["observables"]:
        fig, ax = plt.subplots()

        def update(frame):
            if frame >= config["frames"]:
                return
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
                ants_alive = 0
                productive_ants = 0
                for ant in ant_list:
                    ant.next_step(frame)
                    if not ant.dead:
                        total_energy_consumed += 1
                        ants_alive += 1
                    total_successful_trips += ant.success_trip
                    total_completed_trips += ant.completed_trip
                    if ant.last_food_trip_length > 0:
                        sum_latest_food_trip_length += ant.last_food_trip_length
                        productive_ants += 1
                if productive_ants == 0:
                    productive_ants = 1
                avg_food_trip_length.append(
                    sum_latest_food_trip_length / productive_ants
                )
                if ants_dead_at_step < 0 and ants_alive == 0:
                    ants_dead_at_step = step
                ant_population.append(ants_alive)

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
            ants_alive = 0
            productive_ants = 0
            for ant in ant_list:
                ant.next_step(step)
                if not ant.dead:
                    ants_alive += 1
                    total_energy_consumed += 1
                total_successful_trips += ant.success_trip
                total_completed_trips += ant.completed_trip
                if ant.last_food_trip_length > 0:
                    sum_latest_food_trip_length += ant.last_food_trip_length
                    productive_ants += 1
            if productive_ants == 0:
                productive_ants = 1
            avg_food_trip_length.append(sum_latest_food_trip_length / productive_ants)
            if ants_dead_at_step < 0 and ants_alive == 0:
                ants_dead_at_step = step
            ant_population.append(ants_alive)

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
        plots.colony_food(food_amounts, cycle, ants_dead_at_step)

    if "ant_efficiency" in config["observables"]:
        plots.ant_efficiency(ants_efficiency, cycle, ants_dead_at_step)

    if "success_trips_rate" in config["observables"]:
        plots.ant_trip_success_rate(success_trip_rate, cycle, ants_dead_at_step)

    if "visited_area" in config["observables"]:
        plots.visited_area(visited_area, cycle, ants_dead_at_step)

    if "avg_latest_success_trip" in config["observables"]:
        plots.average_steps_per_ant(avg_food_trip_length, cycle, ants_dead_at_step)

    if "plot_paths" in config["observables"]:
        plots.plot_paths_on_grid(environment, all_successful_paths, cycle)

    if "population" in config["observables"]:
        plots.plot_population(ant_population, cycle, ants_dead_at_step)

    # Printed Output
    print(f"Cycle: {cycle}")
    if "time_to_first_path" in config["observables"]:
        if environment.food_at_nest_instances:
            time_to_first_path = min(s for _, s in environment.food_at_nest_instances)
        else:
            time_to_first_path = np.nan
        print("Time to First Path:", time_to_first_path)

    if "time_to_shortest_path" in config["observables"]:
        if environment.best_path_found_step == 0:
            environment.best_path_found_step = np.nan
        print("Time to Shortest Path:", environment.best_path_found_step)

    if "ant_shortest_path_len" in config["observables"]:
        if environment.best_path_length == float("inf"):
            environment.best_path_length = np.nan
        print(f"Shortest Path Length found by Ants: {environment.best_path_length - 1}")

    print("=========================")

    food_amount_amounts.append(food_amounts)
    ants_efficiency_efficiencies.append(ants_efficiency)
    success_trip_rate_rate.append(success_trip_rate)
    visited_amounts.append(visited_area)
    time_to_firsts.append(time_to_first_path)
    time_to_shortests.append(environment.best_path_found_step)
    shortest_ant_paths.append(environment.best_path_length - 1)
    populations.append(ant_population)
    all_successful_paths_ever.append(all_successful_paths)
    avg_food_trip_lengths.append(avg_food_trip_length)

plots.plot_global_paths_on_grid(environment, all_successful_paths_ever)

real_shortest_path = float("inf")
for i, path in enumerate(environment.real_shortest_paths):
    real_shortest_path = len(path)
    print(f"Real Shortest Path Length to Food: {real_shortest_path}")

# Totals
food_amount_tot = np.array(food_amount_amounts)
ants_efficiency_tot = np.array(ants_efficiency_efficiencies)
success_trip_rate_tot = np.array(success_trip_rate_rate)
visited_amount_tot = np.array(visited_amounts)
time_to_first_path_tot = np.array(time_to_firsts)
time_to_shortest_tot = np.array(time_to_shortests)
shortest_ant_path_tot = np.array(shortest_ant_paths)
population_tot = np.array(populations)
avg_food_trip_tot = np.array(avg_food_trip_lengths)

# Averages
food_amount_avg = np.average(food_amount_tot, axis=0)
ants_efficiency_avg = np.average(ants_efficiency_tot, axis=0)
success_trip_rate_avg = np.average(success_trip_rate_tot, axis=0)
visited_amount_avg = np.average(visited_amount_tot, axis=0)
time_to_first_path_avg = np.nanmean(time_to_first_path_tot)
time_to_shortest_avg = np.nanmean(time_to_shortest_tot)
shortest_ant_path_avg = np.nanmean(shortest_ant_path_tot)
population_avg = np.average(population_tot, axis=0)
avg_food_trip_avg = np.average(avg_food_trip_tot, axis=0)

# Standard Deviations
food_amount_std = np.std(food_amount_tot, axis=0, mean=food_amount_avg) / np.sqrt(
    cycles
)
ants_efficiency_std = np.std(
    ants_efficiency_tot, axis=0, mean=ants_efficiency_avg
) / np.sqrt(cycles)
success_trip_rate_std = np.std(
    success_trip_rate_tot, axis=0, mean=success_trip_rate_avg
) / np.sqrt(cycles)
visited_amount_std = np.std(
    visited_amount_tot, axis=0, mean=visited_amount_avg
) / np.sqrt(cycles)
time_to_first_path_std = np.nanstd(
    time_to_first_path_tot, mean=time_to_first_path_avg
) / np.sqrt(cycles)
time_to_shortest_std = np.nanstd(
    time_to_shortest_tot, mean=time_to_shortest_avg
) / np.sqrt(cycles)
shortest_ant_path_std = np.nanstd(
    shortest_ant_path_tot, mean=shortest_ant_path_avg
) / np.sqrt(cycles)
population_std = np.std(population_tot, axis=0, mean=population_avg) / np.sqrt(cycles)
avg_food_trip_std = np.std(avg_food_trip_tot, axis=0, mean=avg_food_trip_avg) / np.sqrt(
    cycles
)

print(
    f"Average Time to First Path: {time_to_first_path_avg} +/- {round(time_to_first_path_std, 2)}"
)
print(
    f"Average Time to Shortest Path: {time_to_shortest_avg} +/- {round(time_to_shortest_std, 2)}"
)
print(
    f"Average Shortest Path Length found by Ants: {shortest_ant_path_avg} +/- {round(shortest_ant_path_std, 2)}"
)
print("=========================")

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

# Population plot
plt.figure(figsize=(8, 5))
plt.plot(x, population_avg, label="Ant Population Avg", color="orange")
plt.fill_between(
    x,
    population_avg - population_std,
    population_avg + population_std,
    color="orange",
    alpha=0.3,
    label="Std Dev",
)
plt.title("Ant Population: Avg Over Cycles")
plt.xlabel("Step")
plt.ylabel("Number of Ants Alive")
plt.legend()
plt.savefig("images/global_population.png")
plt.close()

# Average Latest Food Trip plot
plt.figure(figsize=(8, 5))
plt.plot(x, avg_food_trip_avg, label="Avg Food Trip Length per Ant", color="deeppink")
plt.fill_between(
    x,
    avg_food_trip_avg - avg_food_trip_std,
    avg_food_trip_avg + avg_food_trip_std,
    color="deeppink",
    alpha=0.3,
    label="Std Dev",
)
plt.axhline(
    y=real_shortest_path, color="blue", linestyle="--", label="Real Shortest Path"
)
plt.title("Average Length of Successful Trips: Avg Over Cycles")
plt.xlabel("Step")
plt.ylabel("Length of Latest Successful Trips / Total Ants")
plt.legend()
plt.savefig("images/global_avg_latest_success_trip.png")
plt.close()

# Simulate Best Path
best_food = config["colony_start_amount"]
colony_best_food = []
ants_best_efficiency = []
total_food_collected = 0
total_energy_consumed = 0
for step in range(config["frames"]):
    trip_length = 2 * real_shortest_path
    if step > 0 and step % trip_length == 0:
        total_food_collected += config["num_ants"] * config["ant_carry_amount"]
        total_energy_consumed += config["num_ants"] * trip_length

        best_food += total_food_collected
        best_food -= total_energy_consumed
    colony_best_food.append(best_food)

    efficiency = total_food_collected / (total_energy_consumed + 1e-3)
    ants_best_efficiency.append(round(efficiency, 2))

plots.colony_food(colony_best_food, "best", -1)
plots.ant_efficiency(ants_best_efficiency, "best", -1)

print("Plots saved to the 'images/' folder.")
