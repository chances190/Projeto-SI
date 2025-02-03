from collections import deque
from heapq import heappop, heappush
import numpy as np
import random
from genetic import Chromosome

def dfs(game, env, start):
    stack = [start]
    visited = set()
    path = []
    parent = {start: None}

    while stack:
        if not game.update_display():
            return None
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        path.append(current)
        is_food = env.check(current)
        if is_food:
            full_path = []
            while current is not None:
                full_path.append(current)
                current = parent[current]
            return full_path[::-1]

        neighbors = env.get_valid_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in visited:
                env.set_border(neighbor,True)
                stack.append(neighbor)
                parent[neighbor] = current

    return None


def bfs(game, env, start):
    queue = deque([start])
    visited = set()
    path = []
    parent = {start: None}

    while queue:
        if not game.update_display():
            return None

        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        path.append(current)
        is_food = env.check(current)
        if is_food:
            # Reconstruct path
            full_path = []
            while current is not None:
                full_path.append(current)
                current = parent[current]
            return full_path[::-1]

        neighbors = env.get_valid_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                env.set_border(neighbor,True)
                parent[neighbor] = current

    return None


def uniform(game, env, start):
    priority_queue = []
    heappush(priority_queue, (0, start))
    visited = set()
    parent = {start: None}
    cost = {start: 0}

    while priority_queue:
        if not game.update_display():
            return None
        current_cost, current = heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        is_food = env.check(current)
        if is_food:
            # Reconstruct path
            full_path = []
            while current is not None:
                full_path.append(current)
                current = parent[current]
            return full_path[::-1]

        neighbors = env.get_valid_neighbors(current)
        for neighbor in neighbors:
            new_cost = current_cost + env.get_cost(neighbor)
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost
                heappush(priority_queue, (priority, neighbor))
                parent[neighbor] = current
                env.set_border(neighbor,True)

    return None


def greedy(game, env, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    priority_queue = []
    heappush(priority_queue, (0, start))
    visited = set()
    parent = {start: None}

    while priority_queue:
        if not game.update_display():
            return None
        _, current = heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        is_food = env.check(current)
        if current == goal or is_food:
            # Reconstruct path
            full_path = []
            while current is not None:
                full_path.append(current)
                current = parent[current]
            return full_path[::-1]

        neighbors = env.get_valid_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in visited:
                priority = heuristic(neighbor, goal)
                heappush(priority_queue, (priority, neighbor))
                parent[neighbor] = current
                env.set_border(neighbor,True)
    return None


def a_star(game, env, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    priority_queue = []
    heappush(priority_queue, (0, start))
    visited = set()
    parent = {start: None}
    cost = {start: 0}

    while priority_queue:
        if not game.update_display():
            return None
        _, current = heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        is_food = env.check(current)
        if current == goal or is_food:
            # Reconstruct path
            full_path = []
            while current is not None:
                full_path.append(current)
                current = parent[current]
            return full_path[::-1]

        neighbors = env.get_valid_neighbors(current)
        for neighbor in neighbors:
            new_cost = cost[current] + env.get_cost(neighbor)
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heappush(priority_queue, (priority, neighbor))
                parent[neighbor] = current
                env.set_border(neighbor,True)

    return None


def genetic(game, env, start, goal,qtt_generation):
    env.create_chromosomes(start, 10)
    for i in range(len(env.chromosomes)):
        env.chromosomes[i].create_gene(35, 24, 24, 17, 500)

    cost = []
    for i in range(len(env.chromosomes)):
        env.chromosomes[i].generate_path(game, env)
        cost.append(env.chromosomes[i].calculate_cost(env))

    cost_probabilities = (cost/np.sum(cost))
    print(cost_probabilities)
    for i in range(qtt_generation):
        new_chromosomes = []
        for i in range(len(env.chromosomes)):
            chromo_A = random.choices(env.chromosomes, cost_probabilities,k=1)[0]
            chromo_B = random.choices(env.chromosomes, cost_probabilities,k=1)[0]
            new_genes = chromo_A.crossover(chromo_B)
            chromosome_child = Chromosome(start, i, new_genes)
            new_chromosomes.append(chromosome_child)

        env.chromosomes = new_chromosomes

        for i in range(len(env.chromosomes)):
            env.chromosomes[i].generate_path(game, env)
            cost.append(env.chromosomes[i].calculate_cost(env))

        env.reset_genetic_path()
    #for generation in range(qtt_generation):
    
    return env.chromosomes[0].path