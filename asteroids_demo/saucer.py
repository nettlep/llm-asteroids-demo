import pygame
import random
from .config import WHITE, WIDTH, HEIGHT

class Saucer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Vector graphics style: Outline only
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        # Draw a saucer outline
        # Main body ellipse
        pygame.draw.ellipse(self.image, WHITE, [0, 10, 50, 15], 1)
        # Top dome
        pygame.draw.ellipse(self.image, WHITE, [15, 0, 20, 15], 1)
        # Cockpit
        pygame.draw.circle(self.image, WHITE, (25, 10), 5, 1)
        
        self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))

    def update(self):
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        self.rect.center = self.pos
