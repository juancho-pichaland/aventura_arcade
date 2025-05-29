import pygame
from game.constants import WHITE, BLACK, FONT_NAME, SCREEN_WIDTH, SCREEN_HEIGHT

def show_final_screen(screen, stats, assets):
    font = pygame.font.SysFont(FONT_NAME, 36)
    title_font = pygame.font.SysFont(FONT_NAME, 48, bold=True)

    screen.fill(BLACK)

    title = title_font.render("Fin del juego", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    lines = [
        f"Puntaje Total: {stats.get('score', 0)}",
        f"Enemigos eliminados: {stats.get('enemies_defeated', 0)}",
        f"Niveles completados: {stats.get('levels_completed', 0)}",
        f"Items recogidos: {stats.get('items_collected', 0)}",
        "Presiona cualquier tecla para salir"
    ]

    for i, line in enumerate(lines):
        text = font.render(line, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150 + i * 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False
def show_pause_menu(win, font, big_font):
    win.fill((30, 30, 30))
    pause_text = big_font.render("Juego en Pausa", True, (255, 255, 255))
    continue_text = font.render("Presiona C para continuar", True, (255, 255, 255))
    quit_text = font.render("Presiona Q para salir", True, (255, 255, 255))

    win.blit(pause_text, (100, 200))
    win.blit(continue_text, (100, 270))
    win.blit(quit_text, (100, 300))
    pygame.display.update()

def show_game_over():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    font = pygame.font.SysFont(None, 48)
    screen.fill((0, 0, 0))
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (180, 250))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    exit()

def show_victory():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    font = pygame.font.SysFont(None, 48)
    screen.fill((0, 0, 0))
    text = font.render("¡Has ganado!", True, (0, 255, 0))
    screen.blit(text, (180, 250))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    exit()

def show_final_score(win, font, state):
    win.fill((0, 0, 0))
    score_text = font.render(f"Puntaje final: {state['score']}", True, (255, 255, 0))
    health_text = font.render(f"Salud restante: {state['player_health']}", True, (255, 255, 255))
    inventory_text = font.render(f"Inventario: {state['inventory']}", True, (255, 255, 255))
    win.blit(score_text, (150, 200))
    win.blit(health_text, (150, 250))
    win.blit(inventory_text, (150, 300))
    pygame.display.update()
    pygame.time.wait(5000)
