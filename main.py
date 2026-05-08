import pygame, sys
from game import Game
from objects import Character, Platform, Ground

character_list = {
    "chara1": Character((255, 0, 0), (), 0, 0, 10, 30, 2, 3, 2, 5, 5, 2),
    "chara2":Character((0, 0, 255), (), 0, 0, 10, 30, 2, 3, 2, 5, 5, 2),
}

platforms = [Platform(0, 0, 350, 10)]



#Functions
def draw_player(player):
    pygame.draw.rect(screen, player.color, [player.x, player.y, player.width, player.height])
    screen.blit(player.image, player.rect)

def draw_platform(platform_to_draw):
    pygame.draw.rect(screen, (0,0, 0), [platform_to_draw.x, platform_to_draw.y, platform_to_draw.width, platform_to_draw.height])
    screen.blit(platform_to_draw.image, platform_to_draw.rect)

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

    game.update_positions([key.unicode for key in pygame.key.get_pressed()])

    for platform in platforms:
        draw_platform(platform)

    for character in players:
        draw_player(character)





pygame.quit()
sys.exit()