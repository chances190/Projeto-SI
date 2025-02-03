import random
import numpy as np
from config import OBSTACLE, SAND, MUD, WATER, TERRAIN_COST, GRID_SIZE


class Chromosome:
    def __init__(self, position, idx, genes=None, color=None):
        self.position = position
        self.color = color
        self.path = []
        if genes is None:
            self.genes = []
        else:
            self.genes = genes
        self.hit = False
        self.reach = False
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
        dist = heuristic(env.goal, self.path[len(self.path)-1] if len(self.path)>0 else self.position)
        self.cost += dist*6
        if self.hit: self.cost *= 10
        if self.reach: self.cost /= 10

        return 1/self.cost 


    def create_gene(self, a, b, c, d, max_path, debug=None):
        current = self.position
        directions_xy = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.genes.append(random.choice(directions_xy))
        current = self.genes[0]

        for i in range(max_path-1): #env.check(current):
            direction = self.genes[i]
            if direction == (-1,0): 
                probabilities = [a,d,c,b]
            elif direction == (1,0): 
                probabilities = [b,d,c,a]
            elif direction == (0,-1): 
                probabilities = [c,a,b,d]
            elif direction == (0,1): 
                probabilities = [d,a,b,c]

            next_direction = random.choices(directions_xy,probabilities,k=1)[0]
            self.genes.append(next_direction)
            current = next_direction
        
    def generate_path(self, game, env):
        parent = {self.position: None}
        current = self.position

        for position in self.genes:
            if not game.update_display():
                return None
            
            is_food = env.check(current)
            if is_food:
                self.reach=True
                break

            nx, ny = current[0]+position[0], current[1]+position[1]   
            neighbor = (nx,ny)

            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if (env.grid[ny][nx].terrain_type == OBSTACLE):
                    self.hit = True
                    break

                env.chromosomes_path(current, self.id)
                parent[neighbor] = current
                self.path.append(neighbor)
                current = neighbor
                env.set_border(neighbor,True)
            else :
                self.hit = True
                break

        self.cost = self.calculate_cost(env)



    def crossover(self, partner):
            mid = np.random.randint(0,len(self.genes))
            new_genes = self.genes.copy()
            new_genes[mid:] = partner.genes[mid:]
            return new_genes
        
    def mutate(self,probability):
            for i in range(len(self.genes)):
                if random.random()<probability:
                    self.genes[i] = random.choices([(-1, 0), (1, 0), (0, -1), (0, 1)], [0.25,0.25,0.25,0.25], k=1)[0]
            