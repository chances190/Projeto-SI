"""
env.check((x, y)) -> (terrain_type, is_food)
env.get_valid_neighbors((x, y)) -> [(x1, y1), (x2, y2), ..., (xn, yn)]
(Só esses dois métodos atualizam a visualização do algoritmo)

TERRAIN_COST[terrain_type] -> int

A função deve retornar um caminho na forma [(x1, y1), (x2, y2), ..., (xn, yn)]
começando do ponto inicial e terminando no objetivo
"""

from config import TERRAIN_COST


def dfs(env, start):
    return NotImplemented


def bfs(env, start):
    return NotImplemented


def uniform(env, start):
    return NotImplemented


def greedy(env, start, goal):
    return NotImplemented


def a_star(env, start, goal):
    return NotImplemented


def genetic(env, start, goal):
    return NotImplemented
