from queue import PriorityQueue
import pygame
from constants import GRID_SIZE, OBSTACLE, SAND, MUD, WATER,TILE_SIZE,WIDTH,HEIGHT,COLORS
import sys
from map_game import random_position
import random

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Dijkstra:
    def __init__(self, grid):
        self.grid = grid

    def dijkstra_algorithm(self, start, goal):
        collected_food = 0  
        while True: 
            frontier = PriorityQueue()
            frontier.put((0, start))
            came_from = {start: None}
            cost_so_far = {start: 0}

            path_found = False
            while not frontier.empty():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print(f"Comidas coletadas: {collected_food}")
                        pygame.quit()
                        sys.exit()

               
                _, current = frontier.get()

            
                if current == goal:
                    path_found = True
                    break

               
                for neighbor in self.get_neighbors(current):
                    new_cost = cost_so_far[current] + self.get_cost(neighbor)
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        frontier.put((new_cost, neighbor))
                        came_from[neighbor] = current

               
                for row in range(GRID_SIZE):
                    for col in range(GRID_SIZE):
                        rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, COLORS[self.grid[row][col]], rect)

                for pos in came_from.keys():
                    rect = pygame.Rect(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, (173, 216, 230), rect)

                
                agent_rect = pygame.Rect(
                    start[0] * TILE_SIZE, start[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE
                )
                pygame.draw.rect(screen, (0, 255, 0), agent_rect)  # Verde (agente)

                food_rect = pygame.Rect(
                    goal[0] * TILE_SIZE, goal[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE
                )
                pygame.draw.rect(screen, (255, 0, 0), food_rect)  # Vermelho (comida)

                pygame.display.flip()
                clock.tick(30)

            
            if path_found:
                path = []
                current = goal
                while current != start:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()

               
                for pos in path:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            print(f"Comidas coletadas: {collected_food}")
                            pygame.quit()
                            sys.exit()

                    
                    for row in range(GRID_SIZE):
                        for col in range(GRID_SIZE):
                            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                            pygame.draw.rect(screen, COLORS[self.grid[row][col]], rect)

                    
                    for visited in path:
                        rect = pygame.Rect(visited[0] * TILE_SIZE, visited[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, (173, 216, 230), rect)

                  
                    start = pos

                    
                    agent_rect = pygame.Rect(
                        start[0] * TILE_SIZE, start[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    )
                    pygame.draw.rect(screen, (0, 255, 0), agent_rect)  # Verde (agente)

               
                    food_rect = pygame.Rect(
                        goal[0] * TILE_SIZE, goal[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    )
                    pygame.draw.rect(screen, (255, 0, 0), food_rect)  # Vermelho (comida)

                    
                    pygame.display.flip()
                    clock.tick(10)

                
                collected_food += 1
                print(f"Comidas coletadas: {collected_food}")

                # Gerar nova posição para a comida
                goal = random_position()
            else:
                print("Nenhum caminho encontrado!")
                print(f"Comidas coletadas: {collected_food}")
                pygame.quit()
                sys.exit()

    def get_neighbors(self, position):
        x, y = position
        neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.grid[ny][nx] != OBSTACLE:
                neighbors.append((nx, ny))

        return neighbors

    def get_cost(self, position):
        x, y = position
        if self.grid[y][x] == SAND:
            return 1
        elif self.grid[y][x] == MUD:
            return 5
        elif self.grid[y][x] == WATER:
            return 10
        return float('inf')

