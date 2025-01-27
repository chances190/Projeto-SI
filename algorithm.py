
"""
env.check((x, y)) -> (terrain_type, is_food)
env.get_valid_neighbors((x, y)) -> [(x1, y1), (x2, y2), ..., (xn, yn)]
(Só esses dois métodos atualizam a visualização do algoritmo)

TERRAIN_COST[terrain_type] -> int

A função deve retornar um caminho na forma [(x1, y1), (x2, y2), ..., (xn, yn)]
começando do ponto inicial e terminando no objetivo
"""

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
from queue import PriorityQueue
import pygame
from environment import Environment
import sys



def dfs(env, start):
    return NotImplemented


def bfs(env, start):
    return NotImplemented


def uniform_cost(env, start, goal):
    collected_foods = 0
    frontier = PriorityQueue()
    frontier.put((0, start)) 
    came_from = {start: None}  
    cost_so_far = {start: 0}  

    while not frontier.empty():
           
        _, current = frontier.get()

        if current == goal:
            collected_foods +=1 
            print(f"Número de comidas coletadas: {collected_foods}",{collected_foods})
            return reconstruct_path(came_from, start, goal)

        for neighbor in Environment.get_valid_neighbors(env, current):
            new_cost = cost_so_far[current] + Environment.get_cost(env, neighbor)

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                frontier.put((new_cost, neighbor))
                came_from[neighbor] = current

   
    print("Nenhum caminho encontrado entre o ponto inicial e o objetivo.")
    return []


def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:  
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse() 
    return path

def greedy(env, start, goal):
    return NotImplemented


def a_star(env, start, goal):
    return NotImplemented


def genetic(env, start, goal):
    return NotImplemented