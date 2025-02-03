from collections import deque
from heapq import heappop, heappush


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


def genetic(game, env, start, goal):
    env.create_chromosomes(start, 10)
    for i in range(len(env.chromosomes)):
        env.chromosomes[i].create_gene(35, 24, 24, 17, 500)

    for i in range(len(env.chromosomes)):
        env.chromosomes[i].generate_path(game, env)
    #game.draw_environment()
    
    return env.chromosomes[0].path