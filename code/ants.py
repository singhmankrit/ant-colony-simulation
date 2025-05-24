import numpy as np
import random


class Ant:
    def __init__(self, grid):
        self.grid = grid
        self.pos = grid.colony_position  # assume all ants start at colony
        self.path_memory = [self.pos]
        self.pheromone_strength = 0

        # ant status
        self.has_food = False

    def next_step(self, step_number):
        if not self.has_food:
            self.explore_grid()
        else:
            self.travel_back()

        if not self.has_food and self.pos in self.grid.food_positions:
            self.has_food = True
            path_length = len(self.path_memory)
            if path_length > 0:
                self.pheromone_strength = 1 / path_length
            print(f"Ant picked up food at step: {step_number}")

        elif self.pos == self.grid.colony_position:
            if self.has_food:
                self.has_food = False
                print(f"Ant dropped food at step: {step_number}")
            self.path_memory = []
            self.pheromone_strength = 0

        # print("Ant moved to", self.pos)

    def explore_grid(self):
        x, y = self.pos
        directions = [
            (0, 1, 0),
            (1, 0, 1),
            (0, -1, 2),
            (-1, 0, 3),
        ]
        candidates = []  # directions ant can step in and their step score

        for dx, dy, dir in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid.size and 0 <= ny < self.grid.size:
                if (nx, ny) in self.grid.obstacle_positions:  # avoid obstacles
                    continue
                if (
                    len(self.path_memory) > 1 and (nx, ny) == self.path_memory[-2]
                ):  # don't immediately take a step back
                    continue
                # this is for debugging: we can verify that drop time = 2*pickup time in the beginning
                # if (nx, ny) == self.grid.colony_position: # don't come back empty handed
                #     continue

                food_val = self.grid.food_scent[ny, nx]
                pheromone_val = self.grid.food_path[y, x, dir]

                score = 0.1 + food_val + pheromone_val  # step score
                candidates.append(((nx, ny), score))

        if not candidates:
            print("Ant has no legal move")
            return

        # Weighted random selection
        total = sum(score for _, score in candidates)
        probs = [score / total for _, score in candidates]
        chosen_pos = random.choices([pos for pos, _ in candidates], weights=probs)[0]

        # Update path and position
        self.path_memory.append(self.pos)
        self.pos = chosen_pos

    def travel_back(self):
        chosen_pos = self.path_memory.pop()
        self.grid.add_pheromone(
            chosen_pos, calc_dir(chosen_pos, self.pos), strength=self.pheromone_strength
        )
        self.pos = chosen_pos


def calc_dir(old, new):
    ox, oy = old
    nx, ny = new
    if ny - oy == 1:
        return 0
    elif nx - ox == 1:
        return 1
    elif ny - oy == -1:
        return 2
    elif nx - ox == -1:
        return 3
    else:
        raise ValueError("not a single step")
