import numpy as np
from enum import Enum

class CellType(Enum):
    EMPTY = 0
    OBSTACLE = 1
    COLONY = 2
    FOOD = 3

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.food_scent = np.zeros((size, size), dtype=float)
        self.food_path = np.zeros((size, size), dtype=float) # pheromones
        
        self.food_positions = []
        self.obstacles = []
        self.colony_position = None

    def place_colony(self, position):
        self.colony_position = position
        self.grid[position] = CellType.COLONY.value

    def add_food(self, position):
        self.food_positions.append(position)
        self.grid[position] = CellType.FOOD.value

    def add_obstacle(self, position):
        self.obstacles.append(position)
        self.grid[position] = CellType.OBSTACLE.value

