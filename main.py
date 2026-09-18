import pygame, sys, os, json
from game import Game
from game_objects_list import character_list, maps
from menu_script import run_menu, run_pause
#Check out SPINE (engine)

name_list = [character.name for character in character_list.values()]
state = "menu"


keybinds_file = "keybinds.json" #Make this later

#Default Keybinds:
default_keybinds = {
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


platforms = maps["map1"]["platforms"]
ground = maps["map1"]["ground"]

#Functions
def draw_player(player):
    pygame.draw.rect(screen, player.colour, [player.x, player.y, player.width, player.height])

def draw_platform(platform_to_draw):
    pygame.draw.rect(screen, (0,0, 0), [platform_to_draw.x, platform_to_draw.y, platform_to_draw.width, platform_to_draw.height])

def draw_game(players, platforms):
    screen.fill((255, 255, 255))

    for platform in platforms:
        draw_platform(platform)

    for character in players:
        draw_player(character)

def load_keybinds():
    if os.path.exists(keybinds_file):
        try:
            with open(keybinds_file, "r") as f:
                data = json.load(f)
                # Convert string key names back to pygame key constants
                return {action: getattr(pygame, key) for action, key in data.items()}
        except (json.JSONDecodeError, AttributeError, KeyError):
            pass
    return default_keybinds.copy()

def save_keybinds(binds):
    with open(keybinds_file, "w") as f:
        # Store as string names for readability
        json.dump({pygame.key.name(key): action for action, key in binds.items()}, f)

keybinds = load_keybinds()

#Pygame stuff
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Insert Game Name Here')

clock = pygame.time.Clock()
delta_time = clock.tick(60)/1000
running = True
state = None
overstate = "menu"


#Camera stuffs
camera_mode = "Fixed"

while running:
    clock.tick(60)

    if overstate == "menu":
        players = run_menu(screen, clock, keybinds)

        print("MENU RETURNED:", players)

        if players is None:
            running = False
            continue

        print("P1:", players[0], players[0].name)
        print("P2:", players[1], players[1].name)

        game = Game(platforms, players)

        overstate = "game"

    elif overstate == "game":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    overstate = "pause"
                    continue

        all_keys = pygame.key.get_pressed()

        pressed_keys = {
            "1": [keybinds["1"][k] for k in keybinds["1"] if all_keys[k]],
            "2": [keybinds["2"][k] for k in keybinds["2"] if all_keys[k]]
        }

        #if pressed_keys["1"] or pressed_keys["2"]:
        #    print(pressed_keys)

        state = game.update_positions(pressed_keys)

        if state is None:

            draw_game(players, platforms)

        else:
            running = False

        pygame.display.flip()

    elif overstate == "pause":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    overstate = "game"

        draw_game(players, platforms)
        run_pause(screen)


        pygame.display.flip()


    #    print(character_list["chara1"].x, character_list["chara1"].y, character_list["chara1"].vx, character_list["chara1"].vy)
    #    print(character_list["chara2"].x, character_list["chara2"].y, character_list["chara2"].vx, character_list["chara2"].vy)


try:
    print(state.name + " has won!")
except AttributeError:
    print("System exit")

pygame.quit()
sys.exit()