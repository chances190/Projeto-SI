# Projeto de SI

## Instruções

Ambiente de desenvolvimento:
```bash
python3 -m venv env
pip install -r requirements.txt
```

Para executar:
```bash
python3 main.py
```

## Implementação dos algoritmos

As funções dos algoritmos estão no arquivo `algorithms.py` e devem retornar uma lista de coordenadas `[(x1, y1), (x2, y2), ...]`, partindo da posição atual do agente até a posição da comida.

```py
# Para checar uma posição use 
env.is_food(pos)

# Para obter uma lista dos vizinhos válidos use
get_valid_neighbors(pos)
```