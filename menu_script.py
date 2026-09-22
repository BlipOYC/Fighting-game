#+Maps and keybinds if we have time
import pygame, os, json
from game_objects_list import character_list

DEFAULT_KEYBINDS = {
    "1": {
        pygame.K_w: "up",
        pygame.K_s: "down",
        pygame.K_a: "left",
        pygame.K_d: "right",
        pygame.K_q: "dash",
        pygame.K_f: "attack",
        pygame.K_g: "heavy",
    },
    "2": {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
        pygame.K_SLASH: "dash",
        pygame.K_SEMICOLON: "attack",
        pygame.K_QUOTE: "heavy"
    }
}

current_keybinds = DEFAULT_KEYBINDS.copy()

#We will want to do keybinds using a json file that can be accessed by all modules, so that the main module and the menu module can edit the keybinds.
#keybind_file = "keybinds.json"

class Slider:
    def __init__(self, min_val, max_val, width, height, center,
                 filled_color, unfilled_color, knob_color, touch_color, font_color):

        pos = (0, 0)
        self.val_range = (min_val, max_val)
        self.min_val = min_val
        self.max_val = max_val
        self.slider_val = min_val
        self.slider = pygame.Rect(*pos, width, height)
        self.slider.center = center
        self.filled_color = filled_color
        self.unfilled_color = unfilled_color
        self.is_active = False
        self.font = pygame.font.Font(None, 30)
        self.font_color = font_color

        self.knob_color = {
            True: touch_color,
            False: knob_color
        }

        self.knob_height = height + 14
        self.knob = pygame.Rect(pos[0], pos[1] - 7, 10, self.knob_height)
        self.knob.center = center

        self.filled_slider = pygame.Rect(
            self.slider.x,
            self.slider.y,
            self.knob.centerx - self.slider.x,
            height
        )


    def update_slider(self, mouse_pos, mouse_state):
        if self.knob.collidepoint(mouse_pos) and mouse_state[0] and not self.is_active:
            self.is_active = True

        if not self.knob.collidepoint(mouse_pos) and mouse_state[0] and self.is_active:
            self.knob.centerx = mouse_pos[0]
        elif not (self.knob.collidepoint(mouse_pos) and mouse_state[0]) and self.is_active:
            self.is_active = False

        self.knob.centerx = mouse_pos[0] if self.is_active else self.knob.centerx

        if self.knob.x < self.slider.x:
            self.knob.centerx = self.slider.x
        elif self.knob.x > self.slider.right:
            self.knob.x = self.slider.right

        self.filled_slider.width = max(self.knob.x - self.slider.x, 0)

        self.slider_val = max(
            min(
                int(
                    ((self.val_range[1] - self.val_range[0]) / self.slider.w)
                    * (self.knob.centerx - self.slider.x)),
                self.max_val
            ),
            self.min_val
        )

    def draw(self, screen):
        pygame.draw.rect(
            screen, self.unfilled_color, self.slider, border_radius=7
        )
        pygame.draw.rect(
            screen, self.knob_color[self.is_active],
            self.knob, border_radius=5
        )
        pygame.draw.rect(
            screen, self.filled_color,
            self.filled_slider, border_radius=7
        )

class CharaBox:
    def __init__(self, rect, text, font, center=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.confirmed = False
        if center:
            self.rect.center = center

    def draw(self, screen,p1=False,p2=False):
        if p1 and p2:
            colour = (133, 0, 133)
        elif p1:
            colour = (255, 0, 0)
        elif p2:
            colour = (0, 0, 255)
        else:
            colour = (60, 60, 90)

        shadow_rect = self.rect.move(0, 4)
        pygame.draw.rect(screen, (10, 10, 15), shadow_rect, border_radius=10)

        pygame.draw.rect(screen, colour, self.rect, border_radius=10)

        text_surface = self.font.render(self.text, True, "white")
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

class Button:
    def __init__(self, rect, center, text, font):
        self.rect = pygame.Rect(rect)
        self.rect.center = center
        self.text = text
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            colour = (100, 100, 150)
        else:
            colour = (60, 60, 90)

        shadow_rect = self.rect.move(0, 5)
        pygame.draw.rect(screen, (10, 10, 15), shadow_rect, border_radius=10)

        pygame.draw.rect(screen, colour, self.rect, border_radius=10)

        text_surface = self.font.render(self.text, True, "white")
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

def menu_load_keybinds(keybinds_file):
    print(keybinds_file)
    if os.path.exists(keybinds_file):
        try:
            with open(keybinds_file, "r") as f:
                data = json.load(f)
                # Convert string key names back to pygame key constants
                return {action: getattr(pygame, key) for action, key in data.items()}
        except (json.JSONDecodeError, AttributeError, KeyError):
            pass
    return DEFAULT_KEYBINDS.copy()

def menu_save_keybinds(binds, keybinds_file):
    with open(keybinds_file, "w") as f:
        # Store as string names for readability
        json.dump({pygame.key.name(key): action for action, key in binds.items()}, f)

keybinds = menu_load_keybinds("keybinds.json")
selected_action = None #Will store the instruction to be changed via keybinds

def calculate_character_positions(n_char, tot_char, screen_width):
    column_positions = [
        (screen_width // 5) * 1,
        (screen_width // 5) * 2,
        (screen_width // 5) * 3
    ]

    index = n_char
    full_rows = tot_char // 3
    remainder = tot_char % 3
    row = index // 3
    position_in_row = index % 3

    if row < full_rows:
        column = position_in_row
    else:
        if remainder == 1:
            column = 1
        elif remainder == 2:
            if position_in_row == 0:
                column = 0
            else:
                column = 2

    x = column_positions[column]
    y = 120 + row * 80
    return (x, y)

def create_key_positions(current_keybinds, screen_width):
    print(current_keybinds)
    column_positions = [
        (screen_width // 6) * 2,
        (screen_width // 6) * 3,
        (screen_width // 6) * 4,
    ]
    start_row = 120
    row_gap = 60

    for player_idx, moves in enumerate(current_keybinds.items()):
        #We will create the row
        #----------------------------
        #Move first
        if player_idx == 0:
            for idx, item in enumerate(moves[1].items()):
                key, move = item
                key = str(key)
                key_rect = font.render(key, True, (0, 0, 0))
                move_rect = font.render(move, True, (0, 0, 0))
                screen.blit(key_rect, key_rect.get_rect(center=(column_positions[1], start_row + row_gap * idx)))
                screen.blit(move_rect, move_rect.get_rect(center=(column_positions[0], start_row + row_gap * idx)))
        elif player_idx == 1:
            for idx, item in enumerate(moves[1].items()):
                key = str(item[0])
                move_rect = font.render(key, True, (0, 0, 0))
                screen.blit(move_rect, move_rect.get_rect(center=(column_positions[2], start_row + row_gap * idx)))



# noinspection PyInconsistentReturns
# Which for some reason is needed cuz pycharm is fussy
def run_menu(screen, clock, keybinds_file):
    substate = "main_menu"
    p1pos = 1
    p2pos = 3
    p1_selection_flag = False
    p2_selection_flag = False
    info = pygame.display.Info()
    # fontChange
    font = pygame.font.SysFont(None, 40)
    character_boxes = []
    for idx, character in enumerate(character_list):
        x, y = calculate_character_positions(idx, len(character_list), info.current_w)
        character_boxes.append(
            CharaBox((x, y, 150, 50),
                   character_list[character].name,
                   font)
        )


    running = True
    proceed_to_game_flag = False
    volume_slider = Slider(
        0,
        100,
        400,
        10,
        (500, 400),
        (100, 100, 100),
        (150, 150, 150),
        (205, 10, 10),
        (245, 20, 20),
        (0, 0, 0)
    )
    while running:
        screen.fill((200, 200, 200))

        start_button = Button((0, 0, 200, 50), (400, 120), "START GAME", font)
        settings_button = Button((0, 0, 200, 50), (400, 300), "SETTINGS", font)
        quit_button = Button((0, 0, 200, 50), (400, 540), "QUIT", font)
        keybinds_button = Button((0, 0, 200, 50), (400, 300), "KEYBINDS", font)
        return_button = Button((0, 0, 200, 50), (400, 540), "RETURN", font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if substate == "main_menu":
                if start_button.clicked(event):
                    substate = "character_pos"
                if settings_button.clicked(event):
                    substate = "settings"
                if quit_button.clicked(event):
                    pygame.quit()

            elif substate == "settings":
                if return_button.clicked(event):
                    substate = "main_menu"
                if keybinds_button.clicked(event):
                    substate = "keybinds"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        substate = "main_menu"

            elif substate == "keybinds":
                if return_button.clicked(event):
                    substate = "settings"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        substate = "settings"

            elif substate == "character_pos":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        substate = "main_menu"
                    # Player 1
                    if event.key == pygame.K_f:
                        p1_selection_flag = not p1_selection_flag
                    if not p1_selection_flag:
                        if event.key == pygame.K_a:
                            p1pos -= 1
                        elif event.key == pygame.K_d:
                            p1pos += 1
                        elif event.key == pygame.K_w:
                            p1pos -= 3
                        elif event.key == pygame.K_s:
                            p1pos += 3

                    # Player 2
                    if event.key == pygame.K_SEMICOLON:
                        p2_selection_flag = not p2_selection_flag
                    if not p2_selection_flag:
                        if event.key == pygame.K_LEFT:
                            p2pos -= 1
                        elif event.key == pygame.K_RIGHT:
                            p2pos += 1
                        elif event.key == pygame.K_UP:
                            p2pos -= 3
                        elif event.key == pygame.K_DOWN:
                            p2pos += 3

                    p1pos = min(max(p1pos, 1), len(character_list))
                    p2pos = min(max(p2pos, 1), len(character_list))

                    if event.key == pygame.K_RETURN and p1_selection_flag and p2_selection_flag:
                        #FIND OUT WHICH CHARACTERS ARE SELECTED
                        chara1 = character_boxes[p1pos-1].text
                        chara2 = character_boxes[p2pos-1].text
                        player1 = next(
                            char for char in character_list.values()
                            if char.name == chara1
                        )

                        player2 = next(
                            char for char in character_list.values()
                            if char.name == chara2
                        )

                        return [player1, player2]

                if return_button.clicked(event):
                    substate = "main_menu"

        if substate == "main_menu":
            menu_display_rect = font.render("MENU", True, (0, 0, 0))
            #THE MENU DISPLAY RECT WILL BE REPLACED BY A LOGO IN THE FUTURE?

            screen.blit(menu_display_rect, menu_display_rect.get_rect(center=(400, 40)))

            start_button.draw(screen)
            quit_button.draw(screen)
            settings_button.draw(screen)

        elif substate == "settings":
            #Volume slider
            #Edit keybinds
            wip_rect = font.render("SETTINGS", True, (0, 0, 0))
            screen.blit(wip_rect, wip_rect.get_rect(center=(400, 40)))
            mouse_pos = pygame.mouse.get_pos()
            mouse_state = pygame.mouse.get_pressed()

            volume_slider.update_slider(mouse_pos, mouse_state)
            text = volume_slider.font.render(
                f"VOLUME: {volume_slider.slider_val}",
                True,
                volume_slider.font_color
            )

            screen.blit(text, (100, 390))

            keybinds_button.draw(screen)
            volume_slider.draw(screen)
            return_button.draw(screen)

        elif substate == "keybinds":
            wip_rect = font.render("This page will be completed shortly!", True, (0, 0, 0))
            create_key_positions(current_keybinds, info.current_w)
            screen.blit(wip_rect, wip_rect.get_rect(center=(400, 40)))

            if False: #Activate this whenever this key is selected to be changed by keybinds
                pass

            return_button.draw(screen)

        elif substate == "character_pos":
            character_pos_display_rect = font.render("SELECT CHARACTER", True, (0, 0, 0))
            screen.blit(character_pos_display_rect, character_pos_display_rect.get_rect(center=(400, 40)))

            #To edit
            subtitle = font.render("Player 1: WASD + F     Player 2: ARROWS + ;", True, (50, 50, 50))

            screen.blit(subtitle, subtitle.get_rect(center=(400, 95)))
            for idx, box in enumerate(character_boxes):
                #Eventually, perhaps adding the character to the boxes will be a good idea.
                box.draw(screen,
                         p1=(p1pos==idx+1),
                         p2=(p2pos==idx+1)
                         )
            return_button = Button((0, 0, 200, 50), (400, 540), "RETURN", font)
            return_button.draw(screen)


        pygame.display.flip()
        clock.tick(60)

def run_pause(screen):
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(150)  # Affects transparency from 0-255
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    paused_font = pygame.font.SysFont(None, 72)
    text = paused_font.render("PAUSED", True, (255, 255, 255))
    text_rect = text.get_rect(topleft=(20, 20))
    screen.blit(text, text_rect)

    font_small = pygame.font.Font(None, 36)
    text = font_small.render("Press ESC to resume", True, (255, 255, 255))
    text_rect = text.get_rect(topleft=(20, 100))
    screen.blit(text, text_rect)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Menu Testing')

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    substate = "main_menu"

    print(run_menu(screen, clock, keybinds_file="keybinds.json"))