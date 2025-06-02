#!/usr/bin/env python
import numpy as np
import random
import os
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
    environment.pheromone_decay = config["pheromone_decay"]

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

                if extension == "elitist":
                    environment.reinforce_best_path()

                visited_area.append(np.count_nonzero(environment.visited))

                plots.draw_world(ax, environment, ant_list, frame)

            if "total_ants_efficiency" in config["observables"]:
                total_collected = (
                    len(environment.food_at_nest_instances) * config["ant_carry_amount"]
                )

                efficiency = total_collected / (total_energy_consumed + 1e-3)
                ants_efficiency.append(round(efficiency, 2))

            if (
                "ant_trip_success_rate" in config["observables"]
                and total_completed_trips > 0
            ):
                success_trip_rate.append(total_successful_trips / total_completed_trips)

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
            environment.evaporate_pheromones()
            for ant in ant_list:
                ant.next_step(step)
                if not ant.dead:
                    total_energy_consumed += 1
                total_successful_trips += ant.success_trip
                total_completed_trips += ant.completed_trip

            if extension == "elitist":
                environment.reinforce_best_path()

            if "total_ants_efficiency" in config["observables"]:
                total_collected = (
                    len(environment.food_at_nest_instances) * config["ant_carry_amount"]
                )

                efficiency = total_collected / (total_energy_consumed + 1e-3)
                ants_efficiency.append(round(efficiency, 2))

            if (
                "ant_trip_success_rate" in config["observables"]
                and total_completed_trips > 0
            ):
                success_trip_rate.append(total_successful_trips / total_completed_trips)

            visited_area.append(np.count_nonzero(environment.visited))

    if "colony_food" in config["observables"]:
        plots.colony_food(food_amounts, cycle)

    if "total_ants_efficiency" in config["observables"]:
        plots.ant_efficiency(ants_efficiency, cycle)

    if "time_to_first_path" in config["observables"]:
        if environment.food_at_nest_instances:
            time_to_first_path = min(s for _, s in environment.food_at_nest_instances)
        else:
            time_to_first_path = None
        print("Time to First Path:", time_to_first_path)

    if "time_to_shortest_path" in config["observables"]:
        print("Time to Shortest Path:", environment.best_path_found_step)

    if "shortest_path_length" in config["observables"]:
        print("Shortest Path Length:", environment.best_path_length)

    if "ant_trip_success_rate" in config["observables"]:
        plots.ant_trip_success_rate(success_trip_rate, cycle)

    if "area_explored_per_time" in config["observables"]:
        plots.visited_area(visited_area, cycle)

    food_amount_amounts.append(food_amounts)
    ants_efficiency_efficiencies.append(ants_efficiency)
    success_trip_rate_rate.append(success_trip_rate)
    visited_amounts.append(visited_area)


# food_amount_amounts = np.array(food_amount_amounts)
# ants_efficiency_efficiencies = np.array(ants_efficiency_efficiencies)
# success_trip_rate_rate = np.array(success_trip_rate_rate)

# TODO: calculate errors

# TODO: plot results
