import random
import numpy as np
from config import OBSTACLE, SAND, MUD, WATER, TERRAIN_COST

class Chromosome:
    def __init__(self, position, idx, color=None):
        self.position = position
        self.color = color
        self.path = []
        self.genes = []
        self.cost = 0
        self.id = idx
        
    def calculate_cost(self,env):
            def heuristic(a, b):
                return abs(a[0] - b[0]) + abs(a[1] - b[1])
            def normalize(value, a_min, a_max, b_min, b_max):
                return b_min + ((b_max - b_min) / (a_max - a_min)) * (value - a_min)
            
            self.cost = 0
            for (x,y) in self.path:
                self.cost += TERRAIN_COST[env.grid[y][x].terrain_type]
            dist = heuristic(env.goal, self.path[len(self.path)-1])
            self.cost += dist*10
        
    def create_path(self, env, game, a, b, c, d, max_path, debug=None):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        parent = {self.position: None}
        current = self.position
        path = []
        visited = set()
        
        received_probabilities = [a,b,c,d]
        for i in range(max_path): #env.check(current):
            if not game.update_display():
                return None
            
            is_food = env.check(current)
            if is_food:
                break
            neighbors = env.get_valid_neighbors(current)
            
            probabilities = []
            for neighbor in neighbors:#[(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0]+neighbor[0], current[1]+neighbor[1]
                #if neighbor not in visited:
                probabilities.append((heuristic(neighbor, env.goal), neighbor))
                
            env.chromosomes_path(current, self.id)
            ordered_neighbors = sorted(probabilities)
            choice_probabilities = received_probabilities[:len(probabilities)]/np.sum(received_probabilities[:len(probabilities)])
           
            
            neighbor = random.choices(ordered_neighbors, weights=choice_probabilities, k=1)[0][1]
            parent[neighbor] = current
            path.append(neighbor)
            current = neighbor
            env.set_border(neighbor,True)
            
        self.path = path
        self.cost = self.calculate_cost(env)
        
        def crossover(self, partner):
            mid = np.random.randint(0,len(self.genes))
            new_genes = self.genes.copy()
            new_genes[mid:] = partner.genes[mid:]
            return new_genes
        
        def mutate(self,probability):
            for i in range(self.genes):
                if random.random()<probability:
                    self.genes[i] = random.choices([(-1, 0), (1, 0), (0, -1), (0, 1)], [1,1,1,1]/4, k=1)[0]
            