import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrow Key Display")

# Font setup
font = pygame.font.SysFont(None, 72)  # Default font, size 72

# Mapping of arrow keys to Unicode arrow symbols
arrow_symbols = {
    pygame.K_UP: "↑",
    pygame.K_DOWN: "↓",
    pygame.K_LEFT: "←",
    pygame.K_RIGHT: "→"
}

# Current symbol to display
current_symbol = ""

# Clock for FPS control
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detect key press
        if event.type == pygame.KEYDOWN:
            if event.key in arrow_symbols:
                current_symbol = arrow_symbols[event.key]

        # Detect key release (clear display)
        if event.type == pygame.KEYUP:
            if event.key in arrow_symbols:
                current_symbol = ""

    # Fill background
    screen.fill((30, 30, 30))

    # Render and display the current symbol
    if current_symbol:
        text_surface = font.render(current_symbol, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS