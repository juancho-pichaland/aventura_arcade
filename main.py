# main.py
import pygame
import sys
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.level import LevelManager
from game.screens import show_final_screen
from game.utils import load_game_state, save_game_state
from game.assets_loader import Assets


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Aventura Arcade")
    clock = pygame.time.Clock()

    state = load_game_state()
    assets = Assets()

    level_manager = LevelManager(screen, assets, state)

    while level_manager.running:
        level_manager.update()
        level_manager.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    save_game_state(level_manager.get_state())
    show_final_screen(screen, level_manager.get_stats())
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
