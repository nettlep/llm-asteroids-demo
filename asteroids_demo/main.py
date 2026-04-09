import pygame
import random
from .config import WIDTH, HEIGHT, FPS, BLACK, WHITE
from .ship import Ship
from .asteroid import Asteroid
from .bullet import Bullet
from .saucer import Saucer
from .fragment import Fragment

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroids Self-Running Demo (Vector Style)")
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

        # AI: The ship targets an asteroid or saucer
        target_pos = None
        if asteroids:
            target_pos = asteroids.sprites()[0].pos
        elif saucers:
            target_pos = saucers.sprites()[0].pos

        ship.update(target_pos)
        
        # Handle shooting
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

        # Update groups
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
        for s in saucers:
            if pygame.sprite.spritecollideany(s, asteroids):
                s.kill()
                for _ in range(5):
                    f = Fragment(s.pos, pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2)))
                    all_sprites.add(f)
                    fragments.add(f)

        # Collision: Ship vs Asteroids/Saucer
        ship_collision = False
        if pygame.sprite.spritecollide(ship, asteroids, False):
            ship_collision = True
        if saucers and pygame.sprite.spritecollide(ship, saucers, False):
            ship_collision = True

        if ship_collision:
            for _ in range(10):
                f = Fragment(ship.pos, pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3)))
                all_sprites.add(f)
                fragments.add(f)
            ship.respawn()

        # Draw
        screen.fill(BLACK)
        
        # Draw ship thrust flame (Vector style: outline triangle)
        if ship.is_thrusting:
            # A smaller triangle pointing opposite to thrust direction
            flame_points = []
            # Flame tip is at ship pos + thrust dir * small distance
            tip = ship.pos + ship.is_thrust_dir * 10
            # Base of flame at ship pos
            base_offset = 5
            p2 = ship.pos + pygame.Vector2(base_offset, -base_offset).rotate(-ship.angle)
            p3 = ship.pos + pygame.Vector2(-base_offset, -base_offset).rotate(-ship.angle)
            flame_points = [tip, p2, p3]
            pygame.draw.polygon(screen, WHITE, flame_points, 1)

        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
