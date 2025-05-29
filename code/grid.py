import numpy as np
from enum import Enum


COLONY_FOOD_START_AMOUNT = 2500


class CellType(Enum):
    EMPTY = 0
    COLONY = 1
    FOOD = 2
    OBSTACLE = 3


class Grid:
    def __init__(self, size, start_food_amount=COLONY_FOOD_START_AMOUNT):
        self.size = size
        self.food_path = np.zeros((size, size, 4), dtype=float)  # pheromones
        self.grid = np.zeros((size, size), dtype=int)
        self.colony_position = None
        self.food_positions = []
        self.obstacle_positions = []
        self.pheromone_decay = 0.01

        self.food_gathered_instances = []
        self.food_at_nest_instances = []

        self.colony_food = start_food_amount

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

    def try_get_food(self, amount: int) -> int:
        """
        Try to get up to `amount` of the food from the colony,
        return how much could be retrieved
        """
        assert amount > 0
        real_amount = min(self.colony_food, amount)
        self.colony_food -= real_amount
        assert self.colony_food >= 0
        return real_amount
