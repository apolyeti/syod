import pygame 
from utils.globals import PLAYER_RADIUS, BULLET_COLOR

class Bullet:
    def __init__(self, pos, vel, radius, rotation_angle):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.rotation_angle = rotation_angle

    def draw(self, screen):
        pygame.draw.circle(screen, BULLET_COLOR, self.pos, self.radius)

    def move(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt

    # check if bullet has hit the border
    def check_bounds(self, screen):
        bound = 25
        if self.pos[0] < bound:
            self.reflect(pygame.Vector2(1, 0))
            return True
        if self.pos[0] > screen.get_width() - bound:
            self.reflect(pygame.Vector2(1, 0))
            return True
        if self.pos[1] < bound:
            self.reflect(pygame.Vector2(0, 1))
            return True
        if self.pos[1] > screen.get_height() - bound:
            self.reflect(pygame.Vector2(0, 1))
            return True
        return False

    # check if bullet has hit the player
    def check_collision(self, player_pos):
        if ((self.pos[0] - player_pos[0]) ** 2 + (self.pos[1] - player_pos[1]) ** 2) ** 0.5 < self.radius + PLAYER_RADIUS:
            return True
        return False
    
    # handle trajectory of bullets when spawned
    def rotate(self, angle):
        rotated_vel = pygame.Vector2(self.vel).rotate(angle)
        self.vel[0] = rotated_vel[0]
        self.vel[1] = rotated_vel[1]
    
    # handle bouncing off wall
    def reflect(self, normal):
        dot_product = self.vel[0] * normal[0] + self.vel[1] * normal[1]
        reflected_vel = pygame.Vector2(self.vel) - 2 * dot_product * pygame.Vector2(normal)
        self.vel[0] = reflected_vel[0]
        self.vel[1] = reflected_vel[1]
    
