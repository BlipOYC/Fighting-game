#+Maps and keybinds if we have time
import pygame
from game_objects_list import character_list

class CharaBox:
    def __init__(self, rect, text, font, center=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
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

# noinspection PyInconsistentReturns
# Which for some reason is needed cuz pycharm is fussy
def run_menu(screen, clock):
    substate = "main_menu"
    p1pos = 1
    p2pos = 3
    p1_selection_flag = False
    p2_selection_flag = False
    info = pygame.display.Info()
    font = pygame.font.Font(None, 40)
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
    while running:
        screen.fill((200, 200, 200))

        start_button = Button((0, 0, 200, 50), (400, 120), "START GAME", font)
        quit_button = Button((0, 0, 200, 50), (400, 540), "QUIT", font)
        return_button = Button((0, 0, 200, 50), (400, 540), "RETURN", font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if substate == "main_menu":
                if start_button.clicked(event):
                    substate = "character_pos"
                if quit_button.clicked(event):
                    pygame.quit()

            if substate == "character_pos":
                if event.type == pygame.KEYDOWN:

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
            screen.blit(menu_display_rect, menu_display_rect.get_rect(center=(400, 40)))
            start_button = Button((0, 0, 200, 50), (400, 120), "START GAME", font)
            quit_button = Button((0, 0, 200, 50), (400, 540), "QUIT", font)

            start_button.draw(screen)
            quit_button.draw(screen)

        if substate == "character_pos":
            character_pos_display_rect = font.render("SELECT CHARACTER", True, (0, 0, 0))
            screen.blit(character_pos_display_rect, character_pos_display_rect.get_rect(center=(400, 40)))
            for idx, box in enumerate(character_boxes):
                box.draw(screen,
                         p1=(p1pos==idx+1),
                         p2=(p2pos==idx+1)
                         )
            return_button = Button((0, 0, 200, 50), (400, 540), "RETURN", font)
            return_button.draw(screen)



        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Menu Testing')

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    substate = "main_menu"

    print(run_menu(screen, clock))