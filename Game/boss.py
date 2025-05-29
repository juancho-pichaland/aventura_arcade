from game.constants import TILE_SIZE
from game.assets_loader import Assets

class Boss:
    def __init__(self, position, health=100):
        self.pos = position
        self.health = health

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw(self, screen, assets):
        screen.blit(Assets().boss_image, (self.pos[1] * TILE_SIZE, self.pos[0] * TILE_SIZE))