# agent.py
from config import OBSTACLE
import random


class Agent:
    def __init__(self, environment, position):
        self.environment = environment
        self.position = position
        self.path = []

    def reset_path(self):
        self.path = []
        self.current_step = 0

    def move(self, new_position):
        x, y = new_position
        if self.environment.grid[y][x].terrain_type != OBSTACLE:
            # Mark current position as path
            # self.environment.grid[self.position[1]][self.position[0]].is_path = True
            # Mark new position as checked
            self.environment.grid[y][x].checked = True
            self.position = new_position
            return True
        return False

    def move_random(self):
        self.environment.grid[self.position[1]][self.position[0]].checked = True
        neighbors = self.environment.get_valid_neighbors(self.position)
        if neighbors:
            new_position = random.choice(neighbors)
            self.move(new_position)

    def follow_path(self):
        if self.current_step < len(self.path):
            next_pos = self.path[self.current_step]
            if self.move(next_pos):
                self.current_step += 1
            else:
                print("ERRO: Caminho tem obstáculo!")
                self.reset_path()
