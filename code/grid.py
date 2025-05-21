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
        self.grid = np.zeros((size, size), dtype=int)
        self.food_scent = np.zeros((size, size), dtype=float) # natural scent
        self.food_path = np.zeros((size, size), dtype=float) # pheromones
        
        self.colony_position = None
        self.food_positions = []
        self.obstacle_positions = []

    def place_colony(self, position):
        self.colony_position = position
        self.grid[position] = CellType.COLONY.value

    def add_food(self, position):
        self.food_positions.append(position)
        self.grid[position] = CellType.FOOD.value

    def add_obstacle(self, position):
        self.obstacle_positions.append(position)
        self.grid[position] = CellType.OBSTACLE.value

