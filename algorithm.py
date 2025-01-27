"""
Função para checar uma posição: 
    env.check((x, y)) -> (terrain_type, is_food)

Função para pegar os vizinhos válidos de uma posição:
    env.get_valid_neighbors((x, y)) -> [(x1, y1), (x2, y2), ..., (xn, yn)]

Para pegar o custo do terreno:
    env.get_cost((x,y)) -> cost

O algoritmo de busca deve retornar um caminho na forma [(x1, y1), (x2, y2), ..., (xn, yn)]
começando do ponto inicial e terminando no objetivo. 

Se vocês checarem o terreno sem usar essas funções ou retornarem algo diferente
o jogo não vai saber mostrar o que tá sendo buscado. Se for preciso implementar
algo diferente, façam com cuidado pra não quebrar a lógica de display.
"""

from config import TERRAIN_COST


def dfs(env, start):
    return NotImplemented


def bfs(env, start):
    return NotImplemented


def uniform(env, start, goal):
    return NotImplemented


def greedy(env, start, goal):
    return NotImplemented


def a_star(env, start, goal):
    return NotImplemented


def genetic(env, start, goal):
    return NotImplemented
