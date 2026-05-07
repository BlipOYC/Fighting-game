#Coordinates are top-left based
#Inputs will be dicts in the {character: direction} format
#Hopefully it works

def create_hurtboxes():
    return [] #Implement later

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
            previous_bottom = character.y + character.height

            character.apply_gravity()
            character.move(self.inputs[character])

            character.x += character.vx
            character.y += character.vy

            character.grounded = False

            for platform in self.platforms:
                if previous_bottom <= platform.y <= (character.y - character.height):
                    if platform.passable and character.vy < 0:
                        character.y = platform.y + character.height
                        character.vy = 0
                        character.grounded = True





class Platform:
    def __init__(self, x, y, width, height, passable):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.passable = passable

class Character:
    def __init__(self, moveset, x, y, width, height, gravity, ground_acceleration, air_acceleration, grounded_max_move_speed, air_max_move_speed, jump_force):
        self.moveset = moveset
        self.x = x
        self.y = y
        self.grounded = False

        self.hurtboxes = create_hurtboxes()

        self.width = width
        self.height = height

        self.vx = 0
        self.vy = 0

        self.gravity = gravity
        self.ground_acceleration = ground_acceleration
        self.air_acceleration = air_acceleration
        self.grounded_max_move_speed = grounded_max_move_speed
        self.air_max_move_speed = air_max_move_speed
        self.jump_force = jump_force

    def update_moveset(self, updated_moveset):
        #Where applicable (Brawlhalla...)
        self.moveset = updated_moveset

    def jump(self):
        self.vy -= self.jump_force
        self.grounded = False

    def apply_gravity(self):
        if not self.grounded:
            self.vy -= self.gravity
        else:
            self.vy = 0

    def move(self, directions):
        if directions:
            speed_used = self.air_acceleration
            if 'up' in directions:
                self.jump()
            if self.grounded:
                speed_used = self.ground_acceleration
            if 'left' in directions:
                self.vx -= speed_used
            if 'right' in directions:
                self.vx += speed_used
        else:
            pass

class Hitbox:
    def __init__(self, character, x, y, width, height, active_frames):
        self.character = character
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active_frames = active_frames
