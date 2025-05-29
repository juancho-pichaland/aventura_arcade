# game/constants.py

# Dimensiones
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
rows = 15
cols = 15
TILE_SIZE = SCREEN_WIDTH // cols
FPS = 30
FONT_NAME = "Verdana"
# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# Tiles
TILE_WALL = 1
TILE_MEDICINE = 2
TILE_WEAPON = 3
TILE_ENEMY = 4
TILE_FOLLOWER = 5
TILE_BOSS = 6
TILE_EMPTY = 0

# Inventario
def default_inventory():
    return {"medicine": 0, "weapons": 0}

# Niveles
level_definitions = [
    {"walls": 20, "medicines": 3, "weapons": 2, "enemies": 2, "followers": 1},
    {"walls": 25, "medicines": 3, "weapons": 3, "enemies": 4, "followers": 2},
    {"walls": 30, "medicines": 2, "weapons": 4, "enemies": 6, "followers": 3},
]

# Archivos
SAVE_FILE = "savegame.json"

import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Ruta a la carpeta de assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

