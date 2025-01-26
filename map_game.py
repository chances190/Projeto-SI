import pygame
import numpy as np
import math
import random
from constants import WIDTH, HEIGHT, GRID_SIZE, TILE_SIZE, COLORS, OBSTACLE, SAND, MUD, WATER
# Função para gerar ruído Perlin 2D
def perlin_noise(x, y, grad_grid, grid_size):
    # Encontrar as posições de grid (células)
    x0 = int(x) % grid_size
    y0 = int(y) % grid_size
    x1 = (x0 + 1) % grid_size
    y1 = (y0 + 1) % grid_size

    # Vetores de gradientes
    # g00 = grad_grid[y0][x0]
    # g01 = grad_grid[y1][x0]
    # g10 = grad_grid[y0][x1]
    # g11 = grad_grid[y1][x1]

    # Função de interpolação suavizada (Smoothstep)
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    # Interpolação do ruído
    def dot_grid_gradient(ix, iy, x, y):
        dx = x - ix
        dy = y - iy
        return dx * grad_grid[iy][ix][0] + dy * grad_grid[iy][ix][1]

    # Interpolando entre os gradientes
    u = fade(x - x0)
    v = fade(y - y0)

    n00 = dot_grid_gradient(x0, y0, x, y)
    n01 = dot_grid_gradient(x0, y1, x, y)
    n10 = dot_grid_gradient(x1, y0, x, y)
    n11 = dot_grid_gradient(x1, y1, x, y)

    # Interpolando os resultados
    nx0 = (1 - u) * n00 + u * n10
    nx1 = (1 - u) * n01 + u * n11
    nxy = (1 - v) * nx0 + v * nx1

    return nxy


# Função para gerar o mapa com Perlin Noise manual
def generate_map():
    grid = np.zeros((GRID_SIZE, GRID_SIZE))

    # Inicializar a grade de gradientes (vetores aleatórios)
    grad_grid = np.zeros((GRID_SIZE, GRID_SIZE, 2))
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            angle = random.uniform(0, 2 * math.pi)
            grad_grid[y][x] = (math.cos(angle), math.sin(angle))

    # Parâmetros do Perlin Noise
    scale = 0.15  # Ajuste para controlar a "granulosidade" do terreno

    # Gerar o mapa com Perlin Noise
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            # Obter o valor de Perlin Noise para o ponto (x, y)
            value = perlin_noise(x * scale, y * scale, grad_grid, GRID_SIZE)

            # Mapear o valor de Perlin Noise para um dos tipos de terreno
            if value < -0.1:
                grid[y][x] = OBSTACLE
            elif value < 0.2:
                grid[y][x] = SAND
            elif value < 0.35:
                grid[y][x] = MUD
            else:
                grid[y][x] = WATER

    return grid

# Função para posicionar agente ou comida evitando obstáculos
def random_position(grid):
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if grid[y][x] != OBSTACLE:
            return x, y
        

        