import pygame
from random import choice

def overlap(range1, range2):
    start1, end1 = range1
    start2, end2 = range2

    if start1 > end1:
        start1, end1 = end1, start1
    if start2 > end2:
        start2, end2 = end2, start2

    return start1 <= end2 and start2 <= end1


def execute_move(character, inputs):
    pass
    #character_change, true_attack = character.attack(inputs)
    #character_change = what happens to the character themselves after a move is inputted
    #including change in hurtboxes, animation
    #true_attack = actual Attack object of attack
    #character.execute(character_change)


class Game:
    def __init__(self, platforms, characters):
        self.platforms = platforms
        self.characters = characters
        self.game_zone = [ #Let's keep them on screen first
            (0, 0),
            (800, 600),
        ]
        self.inputs = {}

    def check_grounded(self):
        for character in self.characters:
            character.grounded = any(
                overlap(
                    (character.x, character.x + character.width),
                    (platform.x, platform.x + platform.width),
                )
                and character.y - character.height == platform.y
                for platform in self.platforms
            )

    def take_inputs(self, inputs):
        self.inputs = inputs

    def update_positions(self, inputs):
        self.take_inputs(inputs)

        p1, p2 = self.characters[0], self.characters[1]
        if p1.is_alive() and not p2.is_alive():
            return p1
        elif not p1.is_alive() and p2.is_alive():
            return p2
        elif not p1.is_alive() and not p2.is_alive():
            return "Tie"

        for character in self.characters:
            #Add check for OOB
            character_center_x, character_center_y = character.x + character.width//2, character.y + character.height//2
            if not(self.game_zone[0][0] <= character_center_x <= self.game_zone[1][0] and self.game_zone[0][1] <= character_center_y <= self.game_zone[1][1]):
                character.lives -= 1
                character.is_respawning = True
                character.is_intangible = True
                character.respawn_pos = self.pick_respawn_pos(character)
                #Create death effect later


                #TP to top of screen
                character_center_x = character.respawn_pos[0]
                character_center_y = character.respawn_pos[1] + 50
                character.x = character_center_x - character.width//2
                character.y = character_center_y - character.height//2

                #Mention this line: without this, previous player velocity is still applied, potentially forcing characters to die as soon as they respawn by making them glide off-stage
                character.vx = character.vy = 0

                #repawning logic
            if character.is_respawning:
                if not character.grounded:
                    character.y += min(10, character.respawn_pos[1] - character.y)

                else:
                    print(f"{character.name} has respawned!")
                    character.is_respawning = False
                    character.respawn_pos = None
                    character.is_intangible = False



            #Add dash logic
            #Implement timer for when you can dash again, and make it skip the movement/attacking parts of loop

            #dash logic implemented
            if character.is_dashing:
                character.dash_timer -= 1

                if character.dash_timer <= 0:
                    character.is_dashing = False
                    character.intangible = False
            else:
                if "dash" in self.inputs[character.name]:
                    if not character.is_respawning:
                        character.dash(self.inputs[character.name])
                        if character.grounded:
                            character.dash_delay = character.base_dash_delay
                        else:
                            character.dash_delay *= 1.5
                else:
                    character.apply_gravity() #Moved here so gravity does not affect dashing speeds
                    if not character.is_respawning:
                        character.move(self.inputs[character.name])

            prev_x = character.x
            prev_y = character.y

            character.x += character.vx
            character.y += character.vy

            character.grounded = False

            for platform in self.platforms:
                if (
                        character.x < platform.x + platform.width and
                        character.x + character.width > platform.x and
                        character.y < platform.y + platform.height and
                        prev_y + character.height <= platform.y <= character.y + character.height
                ):
                    if character.vy > 0:
                        character.y = platform.y - character.height
                        character.vy = 0
                        character.grounded = True

            if character.grounded:
                character.air_jumps_used = 0
                character.time_since_last_jump = float("inf")
                character.time_on_ground += 1
                character.dash_delay = character.base_dash_delay
            else:
                character.time_since_last_jump += 1
                character.time_on_ground = 0

            character.hurtboxes = character.create_hurtboxes()
            character.time_since_last_dash += 1


        for character in self.characters:
            execute_move(character, inputs)


        self.inputs = []
        return None

    def pick_respawn_pos(self, character):
        spawn_platform = choice(self.platforms)
        return (spawn_platform.x + spawn_platform.width//2, spawn_platform.y - spawn_platform.height - character.height - 60)