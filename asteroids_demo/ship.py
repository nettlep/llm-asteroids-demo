import pygame
import random
import math
from .config import WHITE, WIDTH, HEIGHT
from .bullet import Bullet

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # We'll use a surface with enough padding for rotation
        self.surface_size = 60
        self.original_image = self._create_ship_image()
        self.rect = self.original_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.rotation_speed = 5
        self.acceleration = 0.2
        self.friction = 0.99
        self.last_shot_int = 0
        self.shoot_delay = 100 
        self.is_thrusting = False
        self.is_thrust_dir = pygame.Vector2(0, 0)

    def _create_ship_image(self):
        # Create a surface with enough padding for rotation
        img = pygame.Surface((self.surface_size, self.surface_size), pygame.SRCALPHA)
        
        # The ship's center is (30, 30)
        # We want it to be shorter than before.
        # Previous height was ~50 (from y=5 to y=55). Let's aim for ~40.
        # Tip: (30, 10)
        # Back corners: (30 + 12.75, 50) and (30 - 12.75, 50)
        # This makes it an isosceles triangle.
        # Let's try even shorter: y from 15 to 45.
        points = [(30, 15), (42.75, 45), (17.25, 45)]
        
        # Draw the polygon. Using lines instead of polygon to be EXPLICIT about every edge.
        # We add the first point at the end to close the loop.
        lines = points + [points[0]]
        pygame.draw.lines(img, WHITE, False, lines, 2)
        
        return img

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
                self.is_thrust_ing = True # wait, typo here in my thought, checking previous code
                self.is_thrusting = True
            else:
                self.is_thrust_dir = pygame.Vector2(0, 0)

        self.vel *= self.friction
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        
        self.rect.center = self.pos
        self.image = pygame.transform.rotate(self.original_image, self.transform_angle())
        self.rect = self.image.get_rect(center=self.pos)

    def transform_angle(self):
        # Rotation in pygame is counter-clockwise, but our angle calculation is based on math.atan2
        # The previous working version used self.angle directly.
        return self.angle

    def shoot_logic(self):
        if random.random() < 0.05:
            now = pygame.time.get_ticks()
            if now - self.last_shot_int > self.shoot_delay:
                direction = pygame.Vector2(0, -1).rotate(-self.rel_angle())
                self.last_shot_int = now
                return Bullet(self.pos, direction)
        return None

    def rel_angle(self):
        return self.angle
