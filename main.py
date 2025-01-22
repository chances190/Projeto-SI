import pygame
import random
import sys
import math
import numpy as np

# Configurações da janela
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 40  # Tamanho do grid (20x20)
TILE_SIZE = WIDTH // GRID_SIZE

# Tipos de terrenos
OBSTACLE = 0
SAND = 1
MUD = 2
WATER = 3

# Cores dos terrenos
COLORS = {
    OBSTACLE: (50, 50, 50),  # Cinza escuro (obstáculo)
    SAND: (194, 178, 128),  # Bege (areia)
    MUD: (139, 69, 19),  # Marrom (atoleiro)
    WATER: (0, 0, 255),  # Azul (água)
}

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ambiente com Terrenos e Busca")
clock = pygame.time.Clock()

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

# Função principal
def main():
    # Gerar o mapa
    grid = generate_map()

    # Posicionar agente e comida
    agent_pos = random_position(grid)
    food_pos = random_position(grid)

    # Função para mover o agente aleatoriamente
    def move_agent_randomly(agent_pos, grid):
        x, y = agent_pos
        # Escolher um movimento aleatório
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Esquerda, direita, cima, baixo
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            # Verificar se a nova posição está dentro dos limites e não é um obstáculo
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and grid[new_y][new_x] != OBSTACLE:
                return new_x, new_y
        return agent_pos  # Se não mover, retorna a posição atual

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mover o agente aleatoriamente
        agent_pos = move_agent_randomly(agent_pos, grid)

        # Desenhar o mapa
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, COLORS[grid[row][col]], rect)

        # Desenhar o agente
        agent_rect = pygame.Rect(
            agent_pos[0] * TILE_SIZE, agent_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
        pygame.draw.rect(screen, (0, 255, 0), agent_rect)  # Verde (agente)

        # Desenhar a comida
        food_rect = pygame.Rect(
            food_pos[0] * TILE_SIZE, food_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
        pygame.draw.rect(screen, (255, 0, 0), food_rect)  # Vermelho (comida)

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(10)  # Reduzir a velocidade de movimento do agente


if __name__ == "__main__":
    main()
