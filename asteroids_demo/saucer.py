import pygame
import random
from .config import RED, WIDTH, HEIGHT

class Saucer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, RED, [0, 0, 40, 20])
        self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))

    def update(self):
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        self.rect.center = self.pos
