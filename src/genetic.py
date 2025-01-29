import random

class Chromosome:
    def __init__(self, position, color=None):
        self.position = position
        self.color = color
        self.path = []
        self.cost = 0
        
    def create_path(self, env, a, b, c, d):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        parent = {self.position: None}
        current = self.position
        path = []
        visited = set()
        
        while env.check(current):
            neighbors = env.get_valid_neighbors(current)
            probabilities = []
            for neighbor in neighbors:
                #if neighbor not in visited:
                probabilities.append(heuristic(neighbor, env.goal), neighbor)
                print("oi")
                
            ordered_neighbors = sorted(probabilities)
            neighbor = random.choices(ordered_neighbors, [a,b,c,d], k=1)[0][1]
            parent[neighbor] = current
            path.append(neighbor)
            env.set_border(neighbor,True)
            
        self.path = path