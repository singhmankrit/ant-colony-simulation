import numpy as np
import random

class Ant:
    def __init__(self, grid):
        self.grid = grid
        self.pos = grid.colony_position # assume all ants start at colony
        self.path_memory = [self.pos]

        # ant status
        self.has_food = False
        self.drop_pheromones = False

    def next_step(self):
        x, y = self.pos
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(directions)

        for dx, dy in directions: # does random walk, no limits on backtracking yet
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid.size and 0 <= ny < self.grid.size:
                if (nx, ny) in self.grid.obstacle_positions: # avoid obstacles
                    continue
                if not self.has_food and (nx, ny) in self.grid.food_positions: # pick up food
                    self.has_food = True
                    # TODO: Add Drop Pheromones and walk back original path
                if self.has_food and (nx, ny) == self.grid.colony_position: # drop food and forget old path
                    self.has_food = False
                    self.path_memory = []

        self.path_memory.append(self.pos)
        self.pos = (nx, ny)

