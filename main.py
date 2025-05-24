#!/usr/bin/env python
import os
import code.grid as grid
import code.ants as ants
import code.plots as plots
import matplotlib.pyplot as plt
import matplotlib.animation as animation

environment = grid.Grid(9)
environment.place_colony((0, 0))
environment.add_food((6, 6))
environment.set_food_scent()

environment.add_obstacle((4, 2))
environment.add_obstacle((4, 3))
environment.add_obstacle((4, 4))
environment.add_obstacle((3, 4))
environment.add_obstacle((2, 4))
environment.add_obstacle((1, 4))


fig, ax = plt.subplots()
ant_list = [ants.Ant(environment) for _ in range(10)]


def update(frame):
    ax.clear()
    environment.evaporate_pheromones()
    for ant in ant_list:
        ant.next_step(frame)
    plots.draw_world(ax, environment, ant_list, frame)


ani = animation.FuncAnimation(fig, update, frames=300, interval=200)

if not os.path.isdir("images"):
    os.mkdir("images")
ani.save("images/ant_simulation.mp4", writer="ffmpeg")
