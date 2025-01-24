# game.py
import pygame
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    BASE_DELAY,
    GRID_SIZE,
    TILE_SIZE,
    COLOR_MAP,
    TERRAIN_COST,
    AGENT_COLOR,
    FOOD_COLOR,
    ALGORITHMS,
)
from environment import Environment
from agent import Agent
from ui import UI
import algorithm


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pathfinding Simulation")
        self.clock = pygame.time.Clock()

        self.last_move_time = 0

        self.environment = Environment()
        self.agent = Agent(self.environment, self.environment.get_random_position())
        self.ui = UI()

        self.running = True
        self.debug_mode = False
        self.selected_algorithm = "None"
        self.show_algorithm_options = False

    def handle_click(self, pos):
        debug_rect, algo_rect = self.ui.draw_ui_elements(
            self.screen, self.debug_mode, self.selected_algorithm
        )

        if debug_rect.collidepoint(pos):
            self.debug_mode = not self.debug_mode
            self.agent.reset_path()

        if algo_rect.collidepoint(pos):
            self.show_algorithm_options = not self.show_algorithm_options
        elif self.show_algorithm_options:
            option_rects = self.ui.draw_algorithm_options(self.screen)
            for i, rect in enumerate(option_rects):
                if rect.collidepoint(pos):
                    self.selected_algorithm = ALGORITHMS[i]
                    self.show_algorithm_options = False
                    self.agent.reset_path()
                    break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)

    def move_debug(self):
        keys = pygame.key.get_pressed()
        x, y = self.agent.position
        self.environment.grid[y][x].is_path = True

        if keys[pygame.K_w] and y > 0:
            self.agent.move((x, y - 1))
        elif keys[pygame.K_s] and y < GRID_SIZE - 1:
            self.agent.move((x, y + 1))
        elif keys[pygame.K_a] and x > 0:
            self.agent.move((x - 1, y))
        elif keys[pygame.K_d] and x < GRID_SIZE - 1:
            self.agent.move((x + 1, y))

    def run_algorithm(self):
        env = self.environment
        start = self.agent.position
        goal = self.environment.goal
        if self.selected_algorithm == "DFS":
            return algorithm.dfs(env, start)
        elif self.selected_algorithm == "BFS":
            return algorithm.bfs(env, start)
        elif self.selected_algorithm == "Uniform":
            return algorithm.uniform_cost(env, start)
        elif self.selected_algorithm == "Greedy":
            return algorithm.greedy(env, start, goal)
        elif self.selected_algorithm == "A*":
            return algorithm.a_star(env, start, goal)
        elif self.selected_algorithm == "Genetic":
            return algorithm.genetic(env, start, goal)

    def update(self):
        current_time = pygame.time.get_ticks()
        x, y = self.agent.position
        terrain = self.environment.grid[y][x].terrain_type
        move_delay = int(BASE_DELAY * TERRAIN_COST[terrain])
        if current_time - self.last_move_time <= move_delay:
            return

        if self.debug_mode:
            self.move_debug()
        elif self.selected_algorithm == "None":
            self.agent.move_random()
        else:
            if not self.agent.path:
                self.agent.path = self.run_algorithm()
                for x, y in self.agent.path:
                    self.environment.grid[y][x].is_path = True
            self.agent.follow_path()

            pass
        self.last_move_time = current_time

        if self.agent.position == self.environment.goal:
            self.environment.reset()
            self.agent.reset_path()

    def render(self):
        self.screen.fill((255, 255, 255))
        self.draw_environment()
        self.draw_agent()
        self.draw_food()
        self.draw_ui()
        pygame.display.flip()
        self.clock.tick(FPS)

    def draw_environment(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                terrain_id = self.environment.grid[y][x].terrain_type
                color = COLOR_MAP[terrain_id]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

                if self.environment.grid[y][x].checked:
                    overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    overlay.fill((255, 255, 255, 128))
                    self.screen.blit(overlay, rect.topleft)

                if self.environment.grid[y][x].is_path:
                    overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    overlay.fill((255, 0, 0, 128))
                    self.screen.blit(overlay, rect.topleft)

    def draw_agent(self):
        x, y = self.agent.position
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, AGENT_COLOR, rect)

    def draw_food(self):
        x, y = self.environment.goal
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, FOOD_COLOR, rect)

    def draw_ui(self):
        self.ui.draw_ui_elements(self.screen, self.debug_mode, self.selected_algorithm)
        if self.show_algorithm_options:
            self.ui.draw_algorithm_options(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
