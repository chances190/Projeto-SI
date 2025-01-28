# environment.py
from config import OBSTACLE, SAND, MUD, WATER, GRID_SIZE, SCALE, DISTRIBUTION, TERRAIN_COST
from terrain_generation import TerrainGenerator
import numpy as np
import random


class Tile:
    def __init__(self, terrain_type):
        self.terrain_type = terrain_type
        self.checked = False
        self.is_border = False
        self.is_path = False


class Environment:
    def __init__(self):
        self.grid = self.create_grid()
        self.goal = self.get_random_position()

    def create_grid(self):
        noise = TerrainGenerator.generate_perlin_noise(GRID_SIZE, SCALE)
        grid = np.empty((GRID_SIZE, GRID_SIZE), dtype=object)

        min_noise = np.min(noise)
        max_noise = np.max(noise)
        noise_range = max_noise - min_noise

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                value = (noise[y][x] - min_noise) / noise_range  # Normalize value to range [0, 1]
                if value < DISTRIBUTION[OBSTACLE]:
                    terrain = OBSTACLE
                elif value < DISTRIBUTION[OBSTACLE] + DISTRIBUTION[SAND]:
                    terrain = SAND
                elif value < DISTRIBUTION[OBSTACLE] + DISTRIBUTION[SAND] + DISTRIBUTION[MUD]:
                    terrain = MUD
                else:
                    terrain = WATER
                grid[y][x] = Tile(terrain)
        return grid

    def get_random_position(self):
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if self.grid[y][x].terrain_type != OBSTACLE:
                return (x, y)

    def get_valid_neighbors(self, position):
        x, y = position
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if self.grid[ny][nx].terrain_type != OBSTACLE:
                    neighbors.append((nx, ny))
        return neighbors

    def check(self, position):
        x, y = position
        self.grid[y][x].checked = True
        self.set_border(position, False)
        is_food = self.goal == position
        return is_food
    
    def set_border(self, position, boolean):
        x,y = position
        self.grid[y][x].is_border = boolean
        return None

    def get_cost(self, position):
        x, y = position
        self.grid[y][x].checked = True
        return TERRAIN_COST[self.grid[y][x].terrain_type]

    def reset(self):
        self.goal = self.get_random_position()
        for row in self.grid:
            for tile in row:
                tile.checked = False
                tile.is_path = False
                tile.is_border = False
