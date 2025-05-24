import numpy as np


class Grid:
    def __init__(self, size):
        self.size = size
        self.food_path = np.zeros((size, size), dtype=float)  # pheromones

        self.colony_position = None
        self.food_positions = []
        self.obstacle_positions = []

    def place_colony(self, position):
        self.colony_position = position

    def add_food(self, position):
        self.food_positions.append(position)

    def add_obstacle(self, position):
        self.obstacle_positions.append(position)

    def evaporate_pheromones(self, decay_rate=0.01):
        self.food_path *= 1 - decay_rate

    def add_pheromone(self, position, strength=1.0):
        x, y = position
        self.food_path[y, x] += strength
