import pygame
import json
import os

# ------------------ CONFIG ------------------
SETTINGS_FILE = "keybinds_playaround.json"
DEFAULT_BINDS = {
    "Move Left": pygame.K_a,
    "Move Right": pygame.K_d,
    "Jump": pygame.K_SPACE
}
# ---------------------------------------------
pygame.init()
screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Keybinding Menu Example")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Load keybinds from file or use defaults
def load_keybinds():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                # Convert string key names back to pygame key constants
                return {action: getattr(pygame, key) for action, key in data.items()}
        except (json.JSONDecodeError, AttributeError, KeyError):
            pass
    return DEFAULT_BINDS.copy()

# Save keybinds to file
def save_keybinds(binds):
    with open(SETTINGS_FILE, "w") as f:
        # Store as string names for readability
        print({action: pygame.key.name(key) for action, key in binds.items()})
        json.dump({action: pygame.key.name(key) for action, key in binds.items()}, f)

keybinds = load_keybinds()

# Menu state
selected_action = None  # Which action is being rebound

def draw_menu():
    screen.fill((30, 30, 30))
    y = 50
    for action, key in keybinds.items():
        text = f"{action}: {pygame.key.name(key)}"
        if selected_action == action:
            text = f"{action}: [Press a key...]"
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (50, y))
        y += 50
    pygame.display.flip()

def get_action_at_pos(pos):
    """Return the action name if clicked on its row."""
    y = 50
    for action in keybinds:
        rect = pygame.Rect(50, y, 400, 40)
        if rect.collidepoint(pos):
            return action
        y += 50
    return None

# ------------------ MAIN LOOP ------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_keybinds(keybinds)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_action = get_action_at_pos(event.pos)
            if clicked_action:
                selected_action = clicked_action

        elif event.type == pygame.KEYDOWN:
            if selected_action:
                # Assign new key
                keybinds[selected_action] = event.key
                selected_action = None
                save_keybinds(keybinds)
            else:
                # Example: using the binds in-game
                if event.key == keybinds["Move Left"]:
                    print("Moving left")
                elif event.key == keybinds["Move Right"]:
                    print("Moving right")
                elif event.key == keybinds["Jump"]:
                    print("Jumping")

    draw_menu()
    clock.tick(60)

pygame.quit()