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

class Tile:
    def __init__(self, terrain_type):
        self.terrain_type = terrain_type
        self.visits = 0

class Environment:
    def __init__(self):
        self.grid = self._generate_grid()

    def _generate_grid(self):
        grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=object)
        grad_grid = np.zeros((GRID_SIZE, GRID_SIZE, 2))
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                angle = random.uniform(0, 2 * math.pi)
                grad_grid[y][x] = (math.cos(angle), math.sin(angle))
        scale = 0.15
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                value = self._perlin_noise(x * scale, y * scale, grad_grid, GRID_SIZE)
                if value < -0.1:
                    grid[y][x] = Tile(OBSTACLE)
                elif value < 0.2:
                    grid[y][x] = Tile(SAND)
                elif value < 0.35:
                    grid[y][x] = Tile(MUD)
                else:
                    grid[y][x] = Tile(WATER)
        return grid

    def _perlin_noise(self, x, y, grad_grid, grid_size):
        # Encontrar as posições de grid (células)
        x0 = int(x) % grid_size
        y0 = int(y) % grid_size
        x1 = (x0 + 1) % grid_size
        y1 = (y0 + 1) % grid_size

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

    def random_valid_position(self):
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if self.grid[y][x].terrain_type != OBSTACLE:
                return x, y

class Food:
    def __init__(self, position):
        self.position = position


class Agent:
    def __init__(self, environment):
        self._env = environment
        self.position = self._env.random_valid_position()

    def move_randomly(self):
        x, y = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < GRID_SIZE
                and 0 <= new_y < GRID_SIZE
                and self._env.grid[new_y][new_x].terrain_type != OBSTACLE
            ):
                self.position = (new_x, new_y)
                self._env.grid[new_y][new_x].visits += 1
                return
        self._env.grid[y][x].visits += 1

    def move_with_wasd(self, keys):
        x, y = self.position
        if keys[pygame.K_w] and y > 0 and self._env.grid[y - 1][x].terrain_type != OBSTACLE:
            y -= 1
        elif (
            keys[pygame.K_s]
            and y < GRID_SIZE - 1
            and self._env.grid[y + 1][x].terrain_type != OBSTACLE
        ):
            y += 1
        elif keys[pygame.K_a] and x > 0 and self._env.grid[y][x - 1].terrain_type != OBSTACLE:
            x -= 1
        elif (
            keys[pygame.K_d]
            and x < GRID_SIZE - 1
            and self._env.grid[y][x + 1].terrain_type != OBSTACLE
        ):
            x += 1
        self.position = (x, y)
        self._env.grid[y][x].visits += 1

    def delay_movement(self):
        x, y = self.position
        terrain_type = self._env.grid[y][x].terrain_type
        terrain_names = ["obstacle", "sand", "mud", "water"]
        print("Current terrain: ", terrain_names[terrain_type])
        pygame.time.delay(int(60 / SPEED_MULTIPLIERS.get(terrain_type, 1)))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ambiente com Terrenos e Busca")
        self.clock = pygame.time.Clock()

        self.environment = Environment()
        self.agent = Agent(self.environment)
        self.food = Food(self.environment.random_valid_position())

        self.debug_mode = False

        self.selected_algorithm = "None"
        self.show_algorithm_options = False

    def draw_map(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(
                    self.screen, COLORS[self.environment.grid[y][x].terrain_type], rect
                )

    def draw_agent(self):
        agent_rect = pygame.Rect(
            self.agent.position[0] * TILE_SIZE,
            self.agent.position[1] * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )
        pygame.draw.rect(self.screen, (255, 0, 0), agent_rect)

    def draw_food(self):
        food_rect = pygame.Rect(
            self.food.position[0] * TILE_SIZE,
            self.food.position[1] * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )
        pygame.draw.rect(self.screen, (0, 255, 0), food_rect)

    def draw_debug_button(self):
        width, height = 120, 30
        x, y = 10, 10
        color = (0, 0, 0, 178)  # 70% opacity black

        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        button_surface.fill(color)
        self.screen.blit(button_surface, (x, y))

        font = pygame.font.Font(None, 24)
        text = font.render(
            "Debug: " + ("ON" if self.debug_mode else "OFF"), True, (255, 255, 255)
        )  # White text
        self.screen.blit(text, (x + 15, y + 8))

        return pygame.Rect(x, y, width, height)  # Returns a button collider to check for clicks

    def draw_algorithm_dropdown(self):
        width, height = 170, 30
        x, y = 10, 50
        color = (0, 0, 0, 178)  # 70% opacity black

        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        button_surface.fill(color)
        self.screen.blit(button_surface, (x, y))

        font = pygame.font.Font(None, 24)
        text = font.render(
            "Algorithm: " + self.selected_algorithm, True, (255, 255, 255)
        )  # White text
        self.screen.blit(text, (x + 15, y + 8))

        return pygame.Rect(x, y, width, height)  # Returns a button collider to check for clicks

    def draw_algorithm_options(self):
        options = ["None", "DFS", "BFS", "Uniform", "Greedy", "A*"]
        width, height = 150, 30
        x, y = 10, 80
        color = (0, 0, 0, 178)  # 70% opacity black

        for i, option in enumerate(options):
            option_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            option_surface.fill(color)
            self.screen.blit(option_surface, (x, y + i * height))

            font = pygame.font.Font(None, 24)
            text = font.render(option, True, (255, 255, 255))  # White text
            self.screen.blit(text, (x + 15, y + 8 + i * height))

        return [pygame.Rect(x, y + i * height, width, height) for i in range(len(options))]

    def handle_algorithm_selection(self, option_rects, mouse_pos):
        options = ["None", "DFS", "BFS", "Uniform", "Greedy", "A*"]
        for i, rect in enumerate(option_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_algorithm = options[i]
                break

    def run(self):
        running = True
        while running:
            # Draw Environment
            self.draw_map()
            self.draw_agent()
            self.draw_food()

            # Handle Agent Movement
            self.agent.delay_movement()
            if self.debug_mode:
                keys = pygame.key.get_pressed()
                self.agent.move_with_wasd(keys)
            else:
                self.agent.move_randomly()

            # Draw GUI
            debug_button_rect = self.draw_debug_button()
            algorithm_dropdown_rect = self.draw_algorithm_dropdown()
            if self.show_algorithm_options:
                option_rects = self.draw_algorithm_options()

            # Handle GUI
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if debug_button_rect.collidepoint(mouse_pos):
                        self.debug_mode = not self.debug_mode
                    elif algorithm_dropdown_rect.collidepoint(mouse_pos):
                        self.show_algorithm_options = not self.show_algorithm_options
                    elif self.show_algorithm_options:
                        self.handle_algorithm_selection(option_rects, mouse_pos)
                        self.show_algorithm_options = False

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()