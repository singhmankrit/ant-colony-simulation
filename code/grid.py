import numpy as np
from enum import Enum


class CellType(Enum):
    EMPTY = 0
    COLONY = 1
    FOOD = 2
    OBSTACLE = 3


class Grid:
    def __init__(self, size):
        self.size = size
        self.food_path = np.zeros((size, size, 4), dtype=float)  # pheromones
        self.grid = np.zeros((size, size), dtype=int)
        self.colony_position = None
        self.food_positions = []
        self.obstacle_positions = []
        self.pheromone_decay = 0.01

    def place_colony(self, position):
        self.colony_position = position
        self.grid[position] = CellType.COLONY.value

    def add_food(self, position):
        self.food_positions.append(position)
        self.grid[position] = CellType.FOOD.value

    def add_obstacle(self, position):
        self.obstacle_positions.append(position)
        self.grid[position] = CellType.OBSTACLE.value

    def evaporate_pheromones(self, decay_rate=0.01):
        self.food_path *= 1 - self.pheromone_decay

    def add_pheromone(self, position, direction, strength=1.0):
        x, y = position
        self.food_path[y, x, direction] += strength
