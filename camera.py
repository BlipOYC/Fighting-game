import pygame

class Camera:
    def __init__(self, centre_x, centre_y, zoom):
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.zoom = zoom
        self.mode = "fixed"

    #These three in case of sudden update needed
    def update_centre(self, x, y):
        self.centre_x = x
        self.centre_y = y

    def update_zoom(self, zoom):
        self.zoom = zoom

    def update_mode(self, mode):
        self.mode = mode

    def match_draw(self, characters, platforms, screen):
        match self.mode:
            case "fixed":
                self.draw_fixed(characters, platforms, screen)
            case "dynamic":
                self.draw_dynamic(characters, platforms, screen)
            case "center":
                self.draw_centered(characters, platforms, screen)
            case _:
                self.draw_fixed(characters, platforms, screen)

    def draw_fixed(self, characters, platforms, screen):
        for character in characters:
            draw_player(character, screen)
        for platform in platforms:
            draw_platform(platform, screen)
        pass

    def draw_dynamic(self, characters, platforms, screen):
        #Leave for last
        pass

    def draw_centered(self, characters, platforms, screen):
        center_x = sum(character.x for character in characters)/len(characters)
        center_y = sum(character.y for character in characters)/len(characters)

        pass


def draw_player(player, screen):
    pygame.draw.rect(screen, player.colour, [player.x, player.y, player.width, player.height])

"""Draws the platforms"""
def draw_platform(platform_to_draw, screen):
    pygame.draw.rect(screen, (0,0, 0), [platform_to_draw.x, platform_to_draw.y, platform_to_draw.width, platform_to_draw.height])

"""Uses both draw_platform and draw_player to create a screen"""
def draw_game(players, platforms, screen):
    #Fetch backgrounds
    screen.fill((255, 255, 255))

    for platform in platforms:
        draw_platform(platform)

    for character in players:
        draw_player(character)