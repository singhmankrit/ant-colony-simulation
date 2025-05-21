import code.grid as grid
import code.ants as ants

environment = grid.Grid(5)
environment.place_colony((0, 0))
environment.add_food((4, 4))

environment.add_obstacle((3, 2))
environment.add_obstacle((3, 3))
environment.add_obstacle((2, 3))
print(environment.grid)

ant = ants.Ant(environment)
for i in range(10):
    ant.next_step()
