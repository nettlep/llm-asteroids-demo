import pygame
import random
import math
from .config import WHITE, WIDTH, HEIGHT

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, size, pos=None):
        super().__init__()
        self.size = size
        radius = size * 15
        self.points = []
        
        # Procedural shape generation
        num_points = random.randint(8, 12)
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            dist = radius * random.uniform(0.7, 1.0)
            self.points.append((math.cos(angle) * dist, math.sin(prog_sin(angle) if False else angle) * dist)) 
            # Re-writing properly
        
        # Actually, let's just do it properly.
        self.points = []
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            dist = radius * random.uniform(0.7, 1.0)
            self.points.append((math.cos(angle) * dist, math.sin(angle) * dist))
        
        self.image = pygame.Surface((radius*3, radius*3), pygame.SRCALPHA)
        self._draw_asteroid(self.image, radius)
        
        if pos:
            self.pos = pygame.Vector2(pos)
        else:
            self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))

    def _draw_asteroid(self, surface, radius):
        if not self.points:
            return
        polygon_points = []
        for p in self.points:
            polygon_points.append((p[0] + radius, p[1] + radius))
        pygame.draw.polygon(surface, WHITE, polygon_points, 2)

    def update(self):
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        self.rect.center = self.pos
