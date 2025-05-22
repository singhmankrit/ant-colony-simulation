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

ant1 = ants.Ant(environment)
ant2 = ants.Ant(environment)
ant3 = ants.Ant(environment)
for i in range(200):
    environment.evaporate_pheromones()
    ant1.next_step()
    ant2.next_step()
    ant3.next_step()
    if i % 10 == 0:
        plots.plot_world(environment, (ant1, ant2, ant3), i)
