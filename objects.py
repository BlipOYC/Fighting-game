import pygame, math
#Coordinates are top-left based
#Inputs will be dicts in the {character: direction} format
#Hopefully it works
def sine(n: float | int) -> float:
    return math.sin(math.radians(n))

def cosine(n):
    return math.cos(math.radians(n))

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
    def __init__(self, archetype, name, colour, moveset, x, y, width, height, gravity, ground_acceleration, air_acceleration, grounded_max_move_speed, air_max_move_speed, jump_force, max_air_jumps, jump_delay):
        self.archetype = archetype
        self.name = name
        self.colour = colour
        self.moveset = moveset
        self.x = x
        self.y = y
        self.grounded = False
        self.percent = 0

        self.width = width
        self.height = height

        self.facing = "right"

        self.hurtboxes = self.create_hurtboxes()

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
        self.can_jump = True

    def change_facing(self):
        if self.vx < 0:
            self.facing = "left"
        elif self.vx > 0:
            self.facing = "right"
        else:
            pass

    def update_moveset(self, updated_moveset):
        #Where applicable (Brawlhalla...)
        self.moveset = updated_moveset

    def jump(self):
        if self.air_jumps_used < self.max_air_jumps and self.time_since_last_jump >= self.jump_delay:
            self.vy = -self.jump_force

            if not self.grounded:
                self.air_jumps_used += 1

            self.grounded = False
            self.time_since_last_jump = 0

            self.can_jump = False


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
            if self.can_jump:
                self.jump()
        else:
            self.can_jump = True

        if 'down' in directions:
            if self.time_on_ground >= 10:
                self.vy += self.gravity
                self.grounded = False
                self.time_on_ground = 0
            elif not self.grounded:
                self.vy += self.air_acceleration

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

    def attack(self, inputs):
        if "attack" in inputs:
            if self.grounded:
                if "down" in inputs:
                    return self.moveset["dLight"]
                elif self.facing in inputs:
                    return self.moveset["fLight"]
                else:
                    return self.moveset["nLight"]
            else:
                if "down" in inputs:
                    return self.moveset["dAir"]
                elif self.facing in inputs:
                    return self.moveset["fAir"]
                elif "up" in inputs:
                    return self.moveset["uAir"]
                else:
                    return self.moveset["nLight"]
        return None

    def execute(self, character_changes):
        pass

    def create_hurtboxes(self):
        return pygame.Rect([self.x, self.y, self.width, self.height])

    def get_hit(self, hitbox): # Add SDI later
        self.percent += hitbox.damage
        #Damage formulas to be WIP based on testing
        if hitbox.fixed_force:
            self.vx = hitbox.force * cosine(hitbox.direction)
            self.vy = hitbox.y * sine(hitbox.direction)
        else:
            self.vx = hitbox.force * cosine(hitbox.direction) * self.percent/10
            self.vy = hitbox.y * sine(hitbox.direction) * self.percent/10

class Attack:
    def __init__(self, associated_hitboxes, owner):
        self.associated_hitboxes = associated_hitboxes
        self.active_ticks = 0
        self.current_hitboxes = [hitbox for hitbox in self.associated_hitboxes if self.active_ticks in hitbox.active_frames]
        self.owner = owner

    def update(self):
        self.active_ticks += 1
        self.current_hitboxes = [hitbox for hitbox in self.associated_hitboxes if self.active_ticks in hitbox.active_frames]

    def collide(self, characters):
        for character in characters:
            if character == self.owner:
                continue
            else:
                hitboxes = sorted(self.current_hitboxes, key=lambda hb: -hb.priority)
                for hitbox in hitboxes:
                    if hitbox.rect.colliderect(character.hurtboxes):
                        character.get_hit(self)
                        return hitbox #So we can apply knockback
                    return None
                return None
        return None


class Hitbox:
    def __init__(self, character, x, y, width, height, active_frames, damage, force, direction, facing, priority=0, fixed_force=False):
        self.character = character
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect([self.x, self.y, self.width, self.height])
        self.active_frames = active_frames #e.g. if attack is inputted, maybe this specific hitbox is active on frames 8 to 9, and appears as (8, 9)
        self.damage = damage
        self.force = force
        self.direction = direction #degrees
        self.facing = facing
        self.priority = priority
        self.fixed_force = fixed_force
