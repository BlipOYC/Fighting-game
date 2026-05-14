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
    def __init__(self, name, colour, moveset, x, y, width, height, gravity, ground_acceleration, air_acceleration, grounded_max_move_speed, air_max_move_speed, jump_force, max_air_jumps, jump_delay):
        self.name = name
        self.colour = colour
        self.moveset = moveset
        self.x = x
        self.y = y
        self.grounded = False
        self.percent = 0

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
        self.max_air_jumps = max_air_jumps
        self.air_jumps_used = 0
        self.jump_delay = jump_delay #Measured in ticks
        self.time_since_last_jump = float("inf") #Measured in ticks
        self.time_on_ground = 0

    def update_moveset(self, updated_moveset):
        #Where applicable (Brawlhalla...)
        self.moveset = updated_moveset

    def jump(self):
        if self.air_jumps_used < self.max_air_jumps and self.time_since_last_jump >= self.jump_delay:
            self.vy -= self.jump_force
            self.grounded = False
            self.air_jumps_used += 1
            self.time_since_last_jump = 0


    def apply_gravity(self):
        if not self.grounded:
            self.vy += self.gravity
        else:
            self.vy = 0

    def move(self, directions):
        accel = self.air_acceleration
        max_speed = self.air_max_move_speed

        if self.grounded:
            accel = self.ground_acceleration
            max_speed = self.grounded_max_move_speed

        if 'up' in directions:
            self.jump()
        if 'down' in directions:
            if self.time_on_ground >= 10:
                self.vy += self.gravity
                self.grounded = False
                self.time_on_ground = 0

        # Target = Horizontal Direction
        target = 0
        if 'left' in directions:
            target -= 1
        if 'right' in directions:
            target += 1

        if target != 0:
            self.vx += target * accel
        else:
            self.vx *= 0.8

        if self.vx > max_speed:
            self.vx = max_speed
        if self.vx < -max_speed:
            self.vx = -max_speed

class Attack:
    def __init__(self, associated_hitboxes):
        self.associated_hitboxes = associated_hitboxes


class Hitbox:
    def __init__(self, character, x, y, width, height, active_frames, damage):
        self.character = character
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active_frames = active_frames
        self.damage = damage
