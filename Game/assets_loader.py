import pygame
import os
from game.constants import ASSETS_DIR, TILE_SIZE

def load_image(filename):
    path = os.path.join(ASSETS_DIR, filename)
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))


class Assets:
    def __init__(self):
        self.player_image = load_image("player.png")
        self.enemy_image = load_image("enemy.png")
        self.follower_image = load_image("follower.png")
        self.boss_image = load_image("boss.png")
        self.weapon_image = load_image("weapon.png")
        self.medicine_image = load_image("medicine.png")
        self.wall_image = load_image("wall.png")
        self.floor_image = load_image("floor.png")
