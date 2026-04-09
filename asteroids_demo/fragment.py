import pygame
import random
from .config import WHITE

class Fragment(pygame.sprite.Sprite):
    def __init__(self, pos, vel):
        super().__init__()
        size = random.randint(2, 5)
        self.image = pygame.Surface((size, size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.vel = vel
        self.lifetime = random.randint(30, 60)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.rect.center + self.vel # Simple movement
        self.rect.center = self.pos
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
