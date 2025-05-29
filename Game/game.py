import pygame
from game.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Game:
    def __init__(self, player, game_map, enemies, follower_enemies, boss):
        self.player = player
        self.map = game_map
        self.enemies = enemies
        self.follower_enemies = follower_enemies
        self.boss = boss
        self.score = 0
        self.font = pygame.font.SysFont(None, 24)

    def draw_map(self, screen, assets):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                screen.blit(assets.get_tile_image(tile), (x * TILE_SIZE, y * TILE_SIZE))

    def draw_entities(self, screen, assets):
        screen.blit(assets.player_image, (self.player.position[1] * TILE_SIZE, self.player.position[0] * TILE_SIZE))
        for enemy in self.enemies:
            screen.blit(assets.enemy_image, (enemy.position[1] * TILE_SIZE, enemy.position[0] * TILE_SIZE))
        for follower in self.follower_enemies:
            screen.blit(assets.follower_image, (follower.position[1] * TILE_SIZE, follower.position[0] * TILE_SIZE))
        if self.boss:
            screen.blit(assets.boss_image, (self.boss.position[1] * TILE_SIZE, self.boss.position[0] * TILE_SIZE))

    def draw_ui(self, screen):
        # Salud
        health_text = self.font.render(f"Salud: {self.player.health}", True, (255, 0, 0))
        screen.blit(health_text, (10, SCREEN_HEIGHT - 20))
        # Armas
        weapon_text = self.font.render(f"Armas: {self.player.weapons}", True, (255, 255, 0))
        screen.blit(weapon_text, (150, SCREEN_HEIGHT - 20))
        # Puntos
        score_text = self.font.render(f"Puntos: {self.score}", True, (0, 255, 0))
        screen.blit(score_text, (300, SCREEN_HEIGHT - 20))

    def update_score(self, amount):
        self.score += amount

    def autosave(self, save_function):
        save_function(self.player, self.map, self.enemies, self.follower_enemies, self.boss, self.score)

    def show_final_screen(self, screen):
        screen.fill((0, 0, 0))
        summary = [
            f"Juego Terminado",
            f"Puntos Totales: {self.score}",
            f"Salud Restante: {self.player.health}",
            f"Armas Restantes: {self.player.weapons}"
        ]
        for i, line in enumerate(summary):
            text = self.font.render(line, True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, 100 + i * 30))
        pygame.display.flip()
        pygame.time.wait(5000)
