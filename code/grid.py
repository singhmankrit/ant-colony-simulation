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

    def set_food_scent(self):
        """
        Sets the food scent levels on the grid based on the positions of food.

        This method updates the `food_scent` array to reflect the scent 
        emitted by food sources. The scent is strongest (value of 1) 
        at the food position, and it decreases with distance. At a 
        distance of 1 cell, the scent is set to 0.5, and at a distance 
        of 2 cells, it is set to 0.25. The scent is only applied within 
        the grid bounds.
        """
        for fx, fy in self.food_positions:
            self.food_scent[fx, fy] = max(self.food_scent[fx, fy], 1)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nx, ny = fx + dx, fy + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        distance = max(abs(dx), abs(dy))
                        if distance == 1:
                            self.food_scent[nx, ny] = max(self.food_scent[nx, ny], 0.5)
                        elif distance == 2:
                            self.food_scent[nx, ny] = max(self.food_scent[nx, ny], 0.25)

