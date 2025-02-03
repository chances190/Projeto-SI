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