# game/player.py
import pygame


class Player:
    def __init__(self, position):
        self.pos = position
        self.health = 100
        self.weapons = 0

    def handle_input(self, key, game_map):
        dx, dy = 0, 0
        if key == pygame.K_UP:
            dx = -1
        elif key == pygame.K_DOWN:
            dx = 1
        elif key == pygame.K_LEFT:
            dy = -1
        elif key == pygame.K_RIGHT:
            dy = 1

        new_x = self.pos[0] + dx
        new_y = self.pos[1] + dy

        # Validar límites y colisiones con paredes
        if 0 <= new_x < len(game_map) and 0 <= new_y < len(game_map[0]):
            if game_map[new_x][new_y] != 1:  # No puede pasar paredes
                self.pos = [new_x, new_y]

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    def add_weapon(self, weapon_name):
        # En este caso solo llevamos la cuenta de la cantidad
        self.weapons += 1

    def draw(self, screen, assets):
        from game.constants import TILE_SIZE
        screen.blit(assets.player_image, (self.pos[1] * TILE_SIZE, self.pos[0] * TILE_SIZE))