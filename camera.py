import pygame

class Camera:
    def __init__(self, centre_x, centre_y, zoom, mode):
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.zoom = zoom
        self.target_zoom = zoom
        self.mode = mode.lower()

    def world_to_screen(self, x, y, screen):
        """Translate to on-screen coords"""
        screen_x = (x - self.centre_x) * self.zoom + screen.get_width() / 2
        screen_y = (y - self.centre_y) * self.zoom + screen.get_height() / 2

        return screen_x, screen_y

    #These three in case of sudden update needed
    def update_centre(self, x, y):
        self.centre_x = x
        self.centre_y = y

    def update_zoom(self, zoom):
        self.zoom = zoom

    def update_mode(self, mode):
        self.mode = mode

    def match_draw(self, characters, platforms, screen):
        if self.zoom > self.target_zoom:
            self.zoom -= min(0.2, self.zoom - self.target_zoom)
        elif self.zoom < self.target_zoom:
            self.zoom += min(0.2, self.target_zoom - self.zoom)

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
            x, y = self.world_to_screen(
                character.x, character.y, screen
            )
            draw_player(character, screen, x, y, self.zoom)

        for platform in platforms:
            x, y = self.world_to_screen(
                platform.x, platform.y, screen
            )
            draw_platform(platform, screen, x, y, self.zoom)

    def draw_dynamic(self, characters, platforms, screen):
        #Leave for last
        if not characters:
            self.draw_fixed(self, characters, platforms, screen)
            return

        #Calculate target for camera
        target_x = sum(character.x for character in characters) / len(characters)
        target_y = sum(character.y for character in characters) / len(characters)

        smoothing = 0.1

        #Hopefully smooth glide?

        self.centre_x += (target_x - self.centre_x) * smoothing
        self.centre_y += (target_y - self.centre_y) * smoothing

        self.draw_fixed(characters, platforms, screen)

    def draw_centered(self, characters, platforms, screen):
        if not self.characters:
            self.draw_fixed(characters, platforms, screen)
            return

        self.center_x = sum(character.x for character in characters)/len(characters)
        self.center_y = sum(character.y for character in characters)/len(characters)

        self.draw_fixed(characters, platforms, screen)
        #Add an updating zoom feature somewhere


def draw_player(player, screen, x, y, zoom):
    #Edit this with respect to current animation
    pygame.draw.rect(screen, player.colour, [x, y, player.width * zoom, player.height * zoom])

"""Draws the platforms"""
def draw_platform(platform_to_draw, screen, x, y, zoom):
    pygame.draw.rect(screen, (0,0, 0), [x, y, platform_to_draw.width * zoom, platform_to_draw.height * zoom])

"""Uses both draw_platform and draw_player to create a screen"""
def draw_game(players, platforms, screen):
    #Fetch backgrounds
    screen.fill((255, 255, 255))

    for platform in platforms:
        draw_platform(platform)

    for character in players:
        draw_player(character)

    pygame.display.flip()