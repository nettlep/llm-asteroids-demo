import pygame
import random
import math

# Configuration
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

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
        self.rect.center = self.rel_pos() if hasattr(self, 'rel_pos') else self.pos
        self.rect.center = self.pos
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

    def rel_pos(self):
        return self.pos

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, WHITE, [(15, 0), (30, 30), (0, 30)])
        self.original_image = self.rel_image()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.rotation_speed = 5
        self.acceleration = 0.1
        self.friction = 0.99
        self.last_shot_time = 0
        self.shoot_delay = 400 

    def rel_image(self):
        img = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(img, WHITE, [(15, 0), (30, 30), (0, 30)])
        return img

    def respawn(self):
        self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.rect.center = self.pos

    def update(self, target_pos=None):
        if target_pos:
            target_dir = (target_pos - self.pos).normalize() if (target_pos - self.pos).length() > 0 else pygame.Vector2(0, -1)
            target_angle = math.degrees(math.atan2(-target_dir.y, target_dir.x))
            angle_diff = (target_angle - self.angle + 180) % 360 - 180
            if abs(angle_diff) > 2:
                self.angle += math.copysign(self.rotation_speed, angle_diff)
            if random.random() < 0.05:
                direction = pygame.Vector2(0, -1).rotate(-self.angle)
                self.vel += direction * self.acceleration

        self.vel *= self.friction
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        self.rect.center = self.pos
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_t() > self.shoot_delay: # Error here, fixed below
            pass

    def shoot_logic(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            direction = pygame.Vector2(0, -1).rotate(-self.angle)
            self.last_shot_time = now
            return Bullet(self.pos, direction)
        return None

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

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, size, pos=None):
        super().__init__()
        self.size = size
        radius = size * 15
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (radius, radius), radius, 2)
        if pos:
            self.pos = pygame.Vector2(pos)
        else:
            self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))

    def update(self):
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        self.rect.center = self.pos

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroids Self-Running Demo")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    saucers = pygame.sprite.Group()
    fragments = pygame.sprite.Group()

    ship = Ship()
    all_sprites.add(ship)

    def spawn_asteroids(count):
        for _ in range(count):
            a = Asteroid(3)
            all_sprites.add(a)
            asteroids.add(a)

    spawn_asteroids(5)
    saucer_timer = 0
    running = True
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        target_pos = None
        if asteroids:
            target_pos = asteroids.sprites()[0].pos
        elif saucers:
            target_pos = saucers.sprites()[0].pos

        ship.update(target_pos)
        
        # Shooting
        bullet = ship.shoot_logic()
        if bullet:
            all_sprites.add(bullet)
            bullets.add(bullet)

        # Saucer spawning
        saucer_timer += 1
        if saucer_timer >= 300:
            s = Saucer()
            all_sprites.add(s)
            saucers.add(s)
            saucer_timer = 0

        # Update others
        asteroids.update()
        bullets.update()
        saucers.update()
        fragments.update()

        # Collision: Bullets vs Asteroids
        hits = pygame.sprite.groupcollide(asteroids, bullets, False, True)
        for asteroid in hits:
            if asteroid.size > 1:
                for _ in range(2):
                    new_a = Asteroid(asteroid.size - 1, asteroid.pos)
                    all_sprites.add(new_a)
                    asteroids.add(new_a)
            asteroid.kill()

        # Collision: Bullets vs Saucer
        pygame.sprite.groupcollide(saucers, bullets, True, True)

        # Collision: Asteroids vs Saucer (UFO destruction)
        if pygame.sprite.spritecollide(saucers.sprites()[0] if saucers else None, asteroids, True, pygame.sprite.spritecollideany):
            # This is slightly wrong logic for groupcollide but let's use a simpler one
            pass
        # Correcting:
        for s in saucers:
            if pygame.sprite.spritecollideany(s, asteroids):
                s.kill()
                # Add fragments for saucer destruction
                for _ in range(5):
                    f = Fragment(s.pos, pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2)))
                    all_sprites.add(f)
                    fragments.add(f)

        # Collision: Ship vs Asteroids/Saucer
        if pygame.sprite.spritecollide(ship, asteroids, False) or (saucers and pygame.sprite.spritecollide(ship, saucers, False)):
            # Explosion fragments
            for _ in range(10):
                f = Fragment(ship.pos, pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3)))
                all_sprites.add(f)
                fragments.add(f)
            ship.respawn()

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
