import pygame
from .config import WHITE

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.vel = direction * 7
        self.lifetime = 60

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
