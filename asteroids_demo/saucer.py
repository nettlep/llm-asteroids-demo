import pygame
import random
from .config import RED, WIDTH, HEIGHT

class Saucer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        # Draw a more "UFO-like" saucer
        pygame.draw.ellipse(self.image, RED, [0, 10, 50, 15])
        pygame.draw.ellipse(self.image, (200, 0, 0), [15, 0, 20, 15])
        pygame.draw.circle(self.image, (100, 0, 0), (25, 10), 5)
        
        self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))

    def update(self):
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        self.rect.center = self.pos
