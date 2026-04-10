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

        # Collision: Asteroids vs Saucer (UF0 destruction)
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
            # The flame should be at the BACK of the ship.
            # The ship's points are relative to (15, 0) as the tip.
            # The back of the ship is the line from (27.75, 30) to (2.25, 30).
            # We want the flame to originate from this back edge and point backwards.
            
            # Let's find the back center point in world space.
            # The ship's rotation is around its center.
            # We need to rotate the relative back center point.
            
            # Relative back center: (15, 30)
            # But the ship's image is 30x30, so the center is (15, 15).
            # The back edge is at y=30. Relative to center, that's (0, 15).
            
            back_center_rel = pygame.Vector2(0, 15)
            back_center_world = ship.pos + back_center_rel.rotate(-ship.angle)
            
            # Thrust direction is pointing away from the ship (backwards).
            # The ship's thrust direction is already calculated in ship.py as 'direction'
            # which is (0, -1).rotate(-ship.angle)
            
            thrust_dir = pygame.Vector2(0, 1).rotate(-ship.angle) # Opposite of ship heading
            
            # Flame is a smaller triangle pointing backwards.
            # Tip of flame: back_center + thrust_dir * 10
            # Base of flame: back_center + some width
            
            tip = back_center_world + thrust_dir * 10
            base_width = 5
            p2 = back_center_world + pygame.Vector2(base_width, 0).rotate(-ship.angle)
            p3 = back_center_world + pygame.Vector2(-base_width, 0).rotate(-ship.angle)
            
            pygame.draw.polygon(screen, WHITE, [tip, p2, p3], 1)

        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
