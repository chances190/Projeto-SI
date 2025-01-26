
import pygame
import random
import sys
import math
import numpy as np
from map_game import random_position, generate_map
from dijkstra import Dijkstra
from constants import WIDTH, HEIGHT, GRID_SIZE, TILE_SIZE, COLORS, OBSTACLE, SAND, MUD, WATER
from queue import PriorityQueue
# Restante do código permanece igual

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ambiente com Terrenos e Busca")
clock = pygame.time.Clock()



# Função principal
def main():
    # Gerar o mapa
    grid = generate_map()

    # Posicionar agente e comida
    agent_pos = random_position(grid)
    food_pos = random_position(grid)

    # Inicializar a busca
    search = Dijkstra(grid)
    search.dijkstra_algorithm(agent_pos,food_pos)


if __name__ == "__main__":
    main()
