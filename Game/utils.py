import pygame
import json
from game.boss import Boss
from game.constants import SAVE_FILE
import os

TILE_COLORS = {
    0: (30, 30, 30),   # empty
    1: (100, 100, 100), # wall
    2: (0, 255, 0),    # medicine
    3: (0, 0, 255),    # weapon
    4: (255, 0, 0),    # enemy
    5: (255, 165, 0),  # follower enemy
    6: (128, 0, 128),  # boss
}

def draw_map(win, state):
    tile_size = win.get_width() // 15
    for i, row in enumerate(state["map"]):
        for j, tile in enumerate(row):
            pygame.draw.rect(win, TILE_COLORS.get(tile, (0, 0, 0)),
                             (j * tile_size, i * tile_size, tile_size, tile_size))
    # Player
    px, py = state["player_pos"]
    pygame.draw.rect(win, (255, 255, 0), (py * tile_size, px * tile_size, tile_size, tile_size))

def draw_hud(win, state, font):
    health = state["player_health"]
    weapons = state["inventory"]["weapons"]
    medicine = state["inventory"]["medicine"]
    score = state["score"]

    pygame.draw.rect(win, (255, 0, 0), (10, 10, 100, 20))
    pygame.draw.rect(win, (0, 255, 0), (10, 10, health, 20))
    text = font.render(f"Health: {health}", True, (255, 255, 255))
    win.blit(text, (120, 10))

    inv_text = font.render(f"Meds: {medicine}  Weaps: {weapons}  Score: {score}", True, (255, 255, 255))
    win.blit(inv_text, (10, 40))

def draw_minimap(win, state):
    minimap_size = 75
    surf = pygame.Surface((minimap_size, minimap_size))
    surf.set_alpha(180)
    tile_size = minimap_size // 15

    for i, row in enumerate(state["map"]):
        for j, tile in enumerate(row):
            color = TILE_COLORS.get(tile, (50, 50, 50))
            pygame.draw.rect(surf, color, (j * tile_size, i * tile_size, tile_size, tile_size))

    px, py = state["player_pos"]
    pygame.draw.rect(surf, (255, 255, 0), (py * tile_size, px * tile_size, tile_size, tile_size))

    win.blit(surf, (win.get_width() - minimap_size - 10, 10))

def save_game(state):
    data = state.copy()
    if isinstance(data["boss"], Boss):
        data["boss"] = {"position": data["boss"].position, "health": data["boss"].health}
    with open("savegame.json", "w") as f:
        json.dump(data, f)

def load_game(state):
    try:
        with open("savegame.json", "r") as f:
            data = json.load(f)
            state.update(data)
            if isinstance(data.get("boss"), dict):
                state["boss"] = Boss(**data["boss"])
    except FileNotFoundError:
        pass


def load_game_state():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_game_state(state):
    with open(SAVE_FILE, 'w') as file:
        json.dump(state, file, indent=4)
