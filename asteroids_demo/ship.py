import pygame
import random
import math
from .config import WHITE, WIDTH, HEIGHT
from .bullet import Bullet

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, WHITE, [(15, 0), (30, 30), (0, 30)])
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.rotation_speed = 5
        self.acceleration = 0.2
        self.friction = 0.99
        self.last_shot_time = 0
        self.shoot_delay = 400 
        self.is_thrusting = False

    def respawn(self):
        self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.rect.center = self.pos

    def update(self, target_pos=None):
        self.is_thrusting = False
        if target_pos:
            target_dir = (target_pos - self.pos).normalize() if (target_pos - self.pos).length() > 0 else pygame.Vector2(0, -1)
            target_angle = math.degrees(math.atan2(-target_dir.y, target_dir.x))
            
            angle_diff = (target_angle - self.angle + 180) % 360 - 180
            if abs(angle_diff) > 2:
                self.angle += math.copysign(self.rotation_speed, angle_diff)

            if random.random() < 0.1:
                direction = pygame.Vector2(0, -1).rotate(-self.angle)
                self.vel += direction * self.acceleration
                self.is_thrust_dir = direction
                self.is_thrusting = True
            else:
                self.is_thrust_dir = pygame.Vector2(0, 0)

        self.vel *= self.friction
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        
        self.rect.center = self.pos
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.padding_rect(self.image, self.pos)

    def padding_rect(self, image, pos):
        rect = image.get_rect(center=pos)
        return rect

    def shoot_logic(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            direction = pygame.Vector2(0, -1).rotate(-self.angle)
            self.last_shot_time = now
            return Bullet(self.pos, direction)
        return None
