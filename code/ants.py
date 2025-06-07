import random
from . import names


class Ant:
    def __init__(
        self,
        grid,
        max_energy,
        max_carry_amount,
        exploration_desire,
        name=None,
        mode="no_backtracking",
    ):
        if name is None:
            name = names.gen_name()
        self.name = name
        self.grid = grid

        # assume all ants start at colony
        self.pos = grid.colony_position
        self.path_memory = [self.pos]

        # ant status
        self.has_food = False
        self.dead = False

        # ant parameters
        self.pheromone_strength = 0
        self.exploration_desire = exploration_desire
        self.energy = max_energy
        self.max_energy = max_energy
        self.carry_amount = max_carry_amount

        self.success_trip = 0
        self.completed_trip = 0
        self.last_food_trip_length = 0
        self.all_successful_paths = []

        # extensions
        self.mode = mode
        self.food_path = []
        self.self_avoid_return = False

    def next_step(self, step_number):
        if self.dead:
            return
        if (self.energy <= 0 or self.self_avoid_return) and self.path_memory:
            # the ant is hungry and will go back to the colony to eat
            self.travel_back()
        elif self.has_food:
            # the ant is carrying food back to the nest
            self.travel_back()
        else:
            # the ant is attempting to gather food
            self.explore_grid()

        self.grid.visited[self.pos] |= True

        if not self.has_food and self.pos in self.grid.food_positions:
            self.has_food = True
            self.food_path = self.path_memory[:]
            self.food_path.append(self.pos)

            self.grid.food_gathered_instances.append((self.name, step_number))
            path_length = len(self.path_memory)
            if path_length > 0:
                self.pheromone_strength = 1 / path_length
            # print(f"\033[94m{self.name}\033[0m picked up food at step: {step_number}")

        elif self.pos == self.grid.colony_position:
            self.completed_trip += 1
            self.self_avoid_return = False
            if self.has_food:
                self.has_food = False
                self.grid.update_best_path(self.food_path, step_number)
                self.grid.colony_food += self.carry_amount
                self.grid.food_at_nest_instances.append((self.name, step_number))
                # print(
                #     f"\033[94m{self.name}\033[0m dropped food at step: {step_number}, there is now \033[92m{self.grid.colony_food}\033[0m at the colony"
                # )
                self.success_trip += 1
                self.last_food_trip_length = len(self.food_path) - 1
                self.all_successful_paths.append(self.food_path)
            self.energy += self.grid.try_get_food(self.max_energy - self.energy)
            if self.energy == 0:
                # print(
                #     f"\033[31m{self.name}\033[0m died from starvation at step: {step_number}"
                # )
                self.dead = True
            self.path_memory = []
            self.pheromone_strength = 0

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
                    self.mode == "no_backtracking"
                    and len(self.path_memory) >= 1
                    and (nx, ny) == self.path_memory[-1]
                ):  # don't immediately take a step back
                    continue
                elif self.mode == "self_avoiding" and (nx, ny) in self.path_memory:
                    continue
                pheromone_val = self.grid.food_path[y, x, dir]

                score = self.exploration_desire + pheromone_val  # step score
                candidates.append(((nx, ny), score))

        if not candidates:
            if self.mode == "no_backtracking":
                nx, ny = self.path_memory[-1]
            if self.mode == "self_avoiding":
                self.self_avoid_return = True
                return

            pheromone_val = self.grid.food_path[
                y, x, calc_dir(self.pos, self.path_memory[-1])
            ]
            score = self.exploration_desire + pheromone_val
            candidates.append(((nx, ny), score))

        # Weighted random selection
        total = sum(score for _, score in candidates)
        probs = [score / total for _, score in candidates]
        chosen_pos = random.choices([pos for pos, _ in candidates], weights=probs)[0]

        # Update path and position
        self.path_memory.append(self.pos)
        self.energy -= 2  # 1 for the step now and 1 for the step going back
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
