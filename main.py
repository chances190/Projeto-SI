import pygame
import random
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

# Speed multipliers based on terrain types
SPEED_MULTIPLIERS = {
    OBSTACLE: 0,  # Cannot move through obstacles
    SAND: 1.0,  # Normal speed on sand
    MUD: 0.5,  # Slower speed on mud
    WATER: 0.25,  # Even slower speed on water
}

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
clock.tick(60)


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

# Draw the Map
def draw_map(grid):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, COLORS[grid[y][x]], rect)


# Draw agent
def draw_agent(agent_pos):
    agent_rect = pygame.Rect(
        agent_pos[0] * TILE_SIZE, agent_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE
    )
    pygame.draw.rect(screen, (255, 0, 0), agent_rect)  # Draw agent in red


# Draw the Debug Mode Toggle Button
def draw_debug_button():
    button_rect = pygame.Rect(10, 10, 120, 30)
    pygame.draw.rect(screen, (200, 200, 200), button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Debug: " + ("ON" if debug_mode else "OFF"), True, (0, 0, 0))
    screen.blit(text, (25, 18))
    return button_rect


# Função para posicionar agente ou comida evitando obstáculos
def random_valid_position(grid):
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if grid[y][x] != OBSTACLE:
            return x, y

# Move Agent Randomly
def move_agent_randomly(agent_pos, grid):
    x, y = agent_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down
    random.shuffle(directions)

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and grid[new_y][new_x] != OBSTACLE:
            return new_x, new_y
    return agent_pos


# Move Agent with WASD
def move_agent_with_wasd(agent_pos, grid, keys):
    x, y = agent_pos
    if keys[pygame.K_w] and y > 0 and grid[y - 1][x] != OBSTACLE:  # Move Up
        y -= 1
    elif keys[pygame.K_s] and y < GRID_SIZE - 1 and grid[y + 1][x] != OBSTACLE:  # Move Down
        y += 1
    elif keys[pygame.K_a] and x > 0 and grid[y][x - 1] != OBSTACLE:  # Move Left
        x -= 1
    elif keys[pygame.K_d] and x < GRID_SIZE - 1 and grid[y][x + 1] != OBSTACLE:  # Move Right
        x += 1
    return x, y


# Delay the agent's movement based on terrain types
def delay_movement(agent_pos, grid):
    x, y = agent_pos
    terrain_type = int(grid[y][x])
    terrain_names = ["obstacle", "sand", "mud", "water"]
    print("Current terrain: ", terrain_names[terrain_type])
    pygame.time.delay(int(60 / SPEED_MULTIPLIERS.get(terrain_type, 1)))


# Main Program
def main():
    grid = generate_map()
    agent_pos = random_valid_position(grid)

    global debug_mode
    debug_mode = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                button_rect = draw_debug_button()
                if button_rect.collidepoint(mouse_pos):
                    debug_mode = not debug_mode  # Toggle debug mode

        # Draw the environment
        screen.fill((255, 255, 255))  # Clear screen with white
        draw_map(grid)
        draw_agent(agent_pos)
        button_rect = draw_debug_button()
        pygame.display.flip()

        # Update agent position
        delay_movement(agent_pos, grid)
        if debug_mode:
            keys = pygame.key.get_pressed()
            agent_pos = move_agent_with_wasd(agent_pos, grid, keys)
        else:
            agent_pos = move_agent_randomly(agent_pos, grid)

    pygame.quit()

if __name__ == "__main__":
    main()