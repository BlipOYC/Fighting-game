import pygame, sys
from game import Game
from game_objects_list import character_list, maps

name_list = ["1", "2"]


keybinds = {
    "1": {
        pygame.K_w: "up",
        pygame.K_s: "down",
        pygame.K_a: "left",
        pygame.K_d: "right",
        pygame.K_f: "attack",
    },
    "2": {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
        pygame.K_SEMICOLON: "attack",
    }
}

platforms = maps["map1"]["platforms"]
ground = maps["map1"]["ground"]

#Functions
def draw_player(player):
    pygame.draw.rect(screen, player.colour, [player.x, player.y, player.width, player.height])

def draw_platform(platform_to_draw):
    pygame.draw.rect(screen, (0,0, 0), [platform_to_draw.x, platform_to_draw.y, platform_to_draw.width, platform_to_draw.height])

#Pygame stuff
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Platform Fighter Prototype')

clock = pygame.time.Clock()
delta_time = 0.1
running = True

#Player stuff
players = [character_list["chara1"], character_list["chara2"]]

#Game thingy
game = Game(platforms, players)

while running:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_keys = pygame.key.get_pressed()

    pressed_keys = {
        "1": [keybinds["1"][k] for k in keybinds["1"] if all_keys[k]],
        "2": [keybinds["2"][k] for k in keybinds["2"] if all_keys[k]]
    }


    game.update_positions(pressed_keys)

    for platform in platforms:
        draw_platform(platform)

    for character in players:
        draw_player(character)

    pygame.display.flip()


#    print(character_list["chara1"].x, character_list["chara1"].y, character_list["chara1"].vx, character_list["chara1"].vy)
#    print(character_list["chara2"].x, character_list["chara2"].y, character_list["chara2"].vx, character_list["chara2"].vy)
    x = character_list["chara1"].air_jumps_used
    y = character_list["chara2"].air_jumps_used
    if x or y:
        print(f"{x}, {y}")


    clock.tick(60)

pygame.quit()
sys.exit()