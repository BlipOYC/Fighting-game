def overlap(range1, range2):
    start1, end1 = range1
    start2, end2 = range2

    if start1 > end1:
        start1, end1 = end1, start1
    if start2 > end2:
        start2, end2 = end2, start2

    return start1 <= end2 and start2 <= end1

class Game:
    def __init__(self, platforms, characters):
        self.platforms = platforms
        self.characters = characters
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

        for character in self.characters:
            character.apply_gravity()
            character.move(self.inputs[character.name])

            character.x += character.vx

            character.y += character.vy

            character.grounded = False

            for platform in self.platforms:
                if (
                        character.x < platform.x + platform.width and
                        character.x + character.width > platform.x and
                        character.y < platform.y + platform.height and
                        character.y + character.height > platform.y
                ):
                    if character.vy > 0:
                        character.y = platform.y - character.height
                        character.vy = 0
                        character.grounded = True

            if character.grounded:
                character.air_jumps_used = 0
                character.time_since_last_jump = float("inf")
                character.time_on_ground += 1
            else:
                character.time_since_last_jump += 1
                character.time_on_ground = 0

            character.hurtboxes = character.create_hurtboxes()

        self.inputs = []