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

# Set simulation parameters
environment.pheromone_decay = config["pheromone_decay"]
seed = config["seed"]

# Initialize
random.seed(seed)
np.random.seed(seed)
mode = config["mode"]

fig, ax = plt.subplots()
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
ants_efficiency = []
total_energy_consumed = 0


def update(frame):
    global total_energy_consumed
    ax.clear()
    food_amounts.append(environment.colony_food)

    if frame == 0:
        plots.draw_world(ax, environment, ant_list, step_number=0)
    else:
        environment.evaporate_pheromones()
        for ant in ant_list:
            ant.next_step(frame)
            if not ant.dead:
                total_energy_consumed += 1

        if extension == "elitist":
            environment.reinforce_best_path()

        plots.draw_world(ax, environment, ant_list, frame)

    if "total_ants_efficiency" in config["observables"]:
        total_collected = (
            len(environment.food_at_nest_instances) * config["ant_carry_amount"]
        )

        efficiency = (total_collected - total_energy_consumed) / (
            total_energy_consumed + total_collected + 1e-3
        )
        ants_efficiency.append(round(efficiency, 2))


# Animate
ani = animation.FuncAnimation(
    fig, update, frames=config["frames"], interval=config["frame_interval"]
)

# Save video
output_path = config["video_output"]
os.makedirs(os.path.dirname(output_path), exist_ok=True)
ani.save(output_path, writer="ffmpeg")

# plots.hist_distances(environment, steps=config["frames"])

if "total_ants_efficiency" in config["observables"]:
    plots.ant_efficiency(ants_efficiency)

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
