import code.grid as grid
import code.ants as ants
import code.plots as plots

environment = grid.Grid(9)
environment.place_colony((0, 0))
environment.add_food((6, 6))
environment.set_food_scent()

environment.add_obstacle((4, 2))
environment.add_obstacle((4, 3))
environment.add_obstacle((4, 4))
environment.add_obstacle((3, 4))
environment.add_obstacle((2, 4))
print(environment.grid)
print("Food Scent: ")
print(environment.food_scent)

ant = ants.Ant(environment)
for i in range(200):
    environment.evaporate_pheromones()
    ant.next_step()
    if i % 10 == 0:
        plots.plot_world(environment, ant, i)
