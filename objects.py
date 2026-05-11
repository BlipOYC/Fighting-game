#Coordinates are top-left based
#Inputs will be dicts in the {character: direction} format
#Hopefully it works
# new commit

def create_hurtboxes():
    return [] #Implement later

class Platform:
    def __init__(self, x, y, width, height, passable):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.passable = passable

class Ground(Platform):
    pass

class Character:
    def __init__(self, name, colour, moveset, x, y, width, height, gravity, ground_acceleration, air_acceleration, grounded_max_move_speed, air_max_move_speed, jump_force):
        self.name = name
        self.colour = colour
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
            self.vy += self.gravity
        else:
            self.vy = 0

    def move(self, directions):
        if directions:
            accel_used = self.air_acceleration
            max_speed = self.air_max_move_speed
            if 'up' in directions:
                self.jump()
            if self.grounded:
                accel_used = self.ground_acceleration
                max_speed = self.grounded_max_move_speed
            if 'left' in directions:
                self.vx = -1 * min(abs(self.vx-accel_used), max_speed)
            if 'right' in directions:
                self.vx += min(abs(self.vx+accel_used), max_speed)
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
