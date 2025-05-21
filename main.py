import code.grid as grid
import code.ants as ants

environment = grid.Grid(5)
environment.add_food((0, 0))
print(environment.grid)

