# config.py

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_SIZE = 40
TILE_SIZE = WINDOW_WIDTH // GRID_SIZE
FPS = 60
BASE_DELAY = 250

# Terrain types
OBSTACLE = 0
SAND = 1
MUD = 2
WATER = 3

# Terrain configuration
SCALE = 0.15
DISTRIBUTION = {OBSTACLE: 0.3, SAND: 0.3, MUD: 0.15, WATER: 0}
COLOR_MAP = {OBSTACLE: (50, 50, 50), SAND: (194, 178, 128), MUD: (139, 69, 19), WATER: (0, 0, 255)}
TERRAIN_COST = {OBSTACLE: float("inf"), SAND: 1.0, MUD: 3.0, WATER: 5.0}

# Agent settings
AGENT_COLOR = (255, 0, 0)
FOOD_COLOR = (0, 255, 0)

# UI settings
UI_BG_COLOR = (0, 0, 0, 178)
UI_TEXT_COLOR = (255, 255, 255)
UI_FONT_SIZE = 24
BUTTON_SIZE = (150, 30)
BUTTON_SPACING = 5

# Algorithms
ALGORITHMS = ["None", "DFS", "BFS", "Uniform", "Greedy", "A*", "Genetic"]
