# terrain_generation.py
import random
import math
import numpy as np


class TerrainGenerator:
    @staticmethod
    def generate_perlin_noise(grid_size, scale):
        grad_grid = np.zeros((grid_size, grid_size, 2))
        for y in range(grid_size):
            for x in range(grid_size):
                angle = random.uniform(0, 2 * math.pi)
                grad_grid[y][x] = (math.cos(angle), math.sin(angle))

        noise_grid = np.zeros((grid_size, grid_size))
        for y in range(grid_size):
            for x in range(grid_size):
                noise_grid[y][x] = TerrainGenerator._perlin_value(
                    x * scale, y * scale, grad_grid, grid_size
                )
        return noise_grid

    @staticmethod
    def _perlin_value(x, y, grad_grid, grid_size):
        x0 = int(x) % grid_size
        y0 = int(y) % grid_size
        x1 = (x0 + 1) % grid_size
        y1 = (y0 + 1) % grid_size

        dx = x - x0
        dy = y - y0

        n00 = grad_grid[y0][x0][0] * dx + grad_grid[y0][x0][1] * dy
        n01 = grad_grid[y1][x0][0] * dx + grad_grid[y1][x0][1] * (dy - 1)
        n10 = grad_grid[y0][x1][0] * (dx - 1) + grad_grid[y0][x1][1] * dy
        n11 = grad_grid[y1][x1][0] * (dx - 1) + grad_grid[y1][x1][1] * (dy - 1)

        u = TerrainGenerator._fade(dx)
        v = TerrainGenerator._fade(dy)

        nx0 = (1 - u) * n00 + u * n10
        nx1 = (1 - u) * n01 + u * n11
        return (1 - v) * nx0 + v * nx1

    @staticmethod
    def _fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)
