import random
from game.constants import TILE_SIZE
from game.assets_loader import Assets

class Enemy:
    def __init__(self, position):
        self.pos = position
        self.health = 30
        self.damage = 5

    def move(self, game_map):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = self.pos[0] + dx
            new_y = self.pos[1] + dy
            if 0 <= new_x < len(game_map) and 0 <= new_y < len(game_map[0]) and game_map[new_x][new_y] == 0:
                self.pos = [new_x, new_y]
                break

    def draw(self, screen, assets):
        screen.blit(Assets().enemy_image, (self.pos[1] * TILE_SIZE, self.pos[0] * TILE_SIZE))

class FollowerEnemy(Enemy):
    def move_towards(self, player_pos, game_map):
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        move_x = 1 if dx > 0 else -1 if dx < 0 else 0
        move_y = 1 if dy > 0 else -1 if dy < 0 else 0

        new_x = self.pos[0] + move_x
        new_y = self.pos[1] + move_y

        if 0 <= new_x < len(game_map) and 0 <= new_y < len(game_map[0]) and game_map[new_x][new_y] == 0:
            self.pos = [new_x, new_y]


    def draw(self, screen, assets):
        screen.blit(Assets().follower_image, (self.pos[1] * TILE_SIZE, self.pos[0] * TILE_SIZE))