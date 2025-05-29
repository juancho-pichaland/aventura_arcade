import pygame
import random
from game.constants import TILE_WALL, TILE_MEDICINE, TILE_WEAPON, TILE_ENEMY, TILE_FOLLOWER, TILE_BOSS, TILE_SIZE, \
    SCREEN_HEIGHT, WHITE
from game.enemy import Enemy, FollowerEnemy
from game.boss import Boss
from game.player import Player


class LevelManager:
    def __init__(self, screen, assets, state):
        self.screen = screen
        self.assets = assets
        self.state = state
        self.running = True
        self.paused = False
        self.frame_count = 0
        self.last_enemy_move = 0
        self.enemy_move_delay = 100

        self.load_state()
        self.generate_level()

    def load_state(self):
        self.current_level = self.state.get("current_level", 0)
        self.player = Player(self.state.get("player_pos", [1, 1]))
        self.score = self.state.get("score", 0)
        self.enemies_defeated = self.state.get("enemies_defeated", 0)
        self.items_collected = self.state.get("items_collected", 0)
        self.levels_completed = self.state.get("levels_completed", 0)
        self.enemies = []
        self.follower_enemies = []
        self.boss = None
        self.map = []

    def generate_level(self):
        rows, cols = 15, 15
        self.map = [[0 for _ in range(cols)] for _ in range(rows)]
        self.place_tiles(TILE_WALL, 40)
        self.place_tiles(TILE_MEDICINE, 5)
        self.place_tiles(TILE_WEAPON, 4)
        self.place_enemies(Enemy, TILE_ENEMY, 5)
        self.place_enemies(FollowerEnemy, TILE_FOLLOWER, 2)

        if self.current_level == 2:
            self.place_boss()

    def place_tiles(self, tile_type, count):
        placed = 0
        while placed < count:
            row, col = random.randint(0, 14), random.randint(0, 14)
            if self.map[row][col] == 0 and [row, col] != self.player.pos:
                self.map[row][col] = tile_type
                placed += 1

    def place_enemies(self, enemy_class, tile_type, count):
        for _ in range(count):
            while True:
                row, col = random.randint(0, 14), random.randint(0, 14)
                if self.map[row][col] == 0 and [row, col] != self.player.pos:
                    self.map[row][col] = tile_type
                    if enemy_class == Enemy:
                        self.enemies.append(Enemy([row, col]))
                    else:
                        self.follower_enemies.append(FollowerEnemy([row, col]))
                    break

    def place_boss(self):
        while True:
            row, col = random.randint(0, 14), random.randint(0, 14)
            if self.map[row][col] == 0 and [row, col] != self.player.pos:
                self.map[row][col] = TILE_BOSS
                self.boss = Boss([row, col])
                break

    def update(self):
        self.handle_events()
        if self.paused:
            return
        self.handle_player_movement()

        now = pygame.time.get_ticks()
        if now - self.last_enemy_move > self.enemy_move_delay:
            self.move_enemies()
            self.last_enemy_move = now

        self.check_collisions()

    def handle_events(self):
        self.move_direction = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    self.move_direction = event.key

    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.handle_input(pygame.K_UP, self.map)
        elif keys[pygame.K_DOWN]:
            self.player.handle_input(pygame.K_DOWN, self.map)
        elif keys[pygame.K_LEFT]:
            self.player.handle_input(pygame.K_LEFT, self.map)
        elif keys[pygame.K_RIGHT]:
            self.player.handle_input(pygame.K_RIGHT, self.map)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move(self.map)
        for follower in self.follower_enemies:
            follower.move_towards(self.player.pos, self.map)
        if self.boss:
            self.boss.update(self.player.pos, self.map)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_map_tiles()
        self.draw_entities()
        self.draw_hud()

        if self.paused:
            self.draw_pause_message()

    def draw_pause_message(self):
        font = pygame.font.SysFont("Verdana", 36)
        pause_text = font.render("Juego en Pausa", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(pause_text, text_rect)

    def draw_map_tiles(self):
        for row, tiles in enumerate(self.map):
            for col, tile in enumerate(tiles):
                pos = (col * TILE_SIZE, row * TILE_SIZE)
                self.screen.blit(self.assets.floor_image, pos)
                if tile == TILE_WALL:
                    self.screen.blit(self.assets.wall_image, pos)
                elif tile == TILE_MEDICINE:
                    self.screen.blit(self.assets.medicine_image, pos)
                elif tile == TILE_WEAPON:
                    self.screen.blit(self.assets.weapon_image, pos)

    def draw_entities(self):
        for enemy in self.enemies:
            enemy.draw(self.screen, self.assets)
        for follower in self.follower_enemies:
            follower.draw(self.screen, self.assets)
        if self.boss:
            self.boss.draw(self.screen, self.assets)
        self.player.draw(self.screen, self.assets)

    def draw_hud(self):
        font = pygame.font.SysFont("Verdana", 18)
        health = font.render(f"Salud: {self.player.health}", True, WHITE)
        score = font.render(f"Puntaje: {self.score}", True, WHITE)
        self.screen.blit(health, (10, SCREEN_HEIGHT - 40))
        self.screen.blit(score, (10, SCREEN_HEIGHT - 20))

    def check_collisions(self):
        row, col = self.player.pos
        tile = self.map[row][col]

        if tile == TILE_MEDICINE:
            self.player.heal(10)
            self.map[row][col] = 0
            self.items_collected += 1
            self.score += 10

        elif tile == TILE_WEAPON:
            self.player.add_weapon("Basic Gun")
            self.map[row][col] = 0
            self.items_collected += 1
            self.score += 15

        self.check_enemy_collisions()
        self.check_boss_collision()

        if self.player.health <= 0:
            self.running = False

        if not self.enemies and not self.follower_enemies and not self.boss:
            self.advance_level()

    def check_enemy_collisions(self):
        for enemy in self.enemies[:]:
            if enemy.pos == self.player.pos:
                self.player.take_damage(10)
                self.enemies.remove(enemy)
                self.enemies_defeated += 1
                self.score += 20

        for follower in self.follower_enemies[:]:
            if follower.pos == self.player.pos:
                self.player.take_damage(15)
                self.follower_enemies.remove(follower)
                self.enemies_defeated += 1
                self.score += 25

    def check_boss_collision(self):
        if self.boss and self.boss.pos == self.player.pos:
            self.player.take_damage(25)
            self.boss.health -= 25
            if self.boss.health <= 0:
                self.score += 100
                self.enemies_defeated += 1
                self.boss = None

    def advance_level(self):
        self.current_level += 1
        self.levels_completed += 1
        self.generate_level()

    def get_state(self):
        return {
            "player_pos": self.player.pos,
            "score": self.score,
            "enemies_defeated": self.enemies_defeated,
            "items_collected": self.items_collected,
            "levels_completed": self.levels_completed,
            "current_level": self.current_level
        }

    def get_stats(self):
        return {
            "score": self.score,
            "enemies_defeated": self.enemies_defeated,
            "items_collected": self.items_collected,
            "levels_completed": self.levels_completed
        }
