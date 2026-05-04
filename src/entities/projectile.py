import pygame
import math
from src.entities.base_entity import Entity


class Projectile(Entity):
    """Základní třída pro všechny střely."""

    def __init__(self, x, y, target_enemy, damage, speed=300):
        super().__init__(x, y, 8, 8)
        self.target = target_enemy
        self.damage = damage
        self.speed = speed
        self.color = (255, 255, 100)

    def update(self, dt: float):
        if not self.target or not self.target.alive:
            self.destroy()
            return

        tx, ty = self.target.center
        cx, cy = self.center
        dx = tx - cx
        dy = ty - cy
        dist = math.hypot(dx, dy)

        if dist < 10:
            self._on_hit()
            self.destroy()
            return

        move = self.speed * dt
        self.x += (dx / dist) * move
        self.y += (dy / dist) * move

    def _on_hit(self):
        """Přepsáno v potomcích – polymorfismus."""
        if self.target and self.target.alive:
            self.target.take_damage(self.damage)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.x + 4), int(self.y + 4)), 4)


class Arrow(Projectile):
    """Šíp z Arrow Tower – rychlý, malé poškození."""
    def __init__(self, x, y, target):
        super().__init__(x, y, target, damage=25, speed=350)
        self.color = (180, 120, 40)

    def draw(self, surface):
        if not self.target or not self.target.alive:
            return
        tx, ty = self.target.center
        cx, cy = self.center
        angle = math.atan2(ty - cy, tx - cx)
        tip_x = cx + math.cos(angle) * 10
        tip_y = cy + math.sin(angle) * 10
        tail_x = cx - math.cos(angle) * 10
        tail_y = cy - math.sin(angle) * 10
        pygame.draw.line(surface, self.color, (int(tail_x), int(tail_y)), (int(tip_x), int(tip_y)), 3)
        pygame.draw.circle(surface, (220, 160, 60), (int(tip_x), int(tip_y)), 3)


class Cannonball(Projectile):
    """Dělová koule – pomalá, velké poškození, plocha."""
    def __init__(self, x, y, target, all_enemies):
        super().__init__(x, y, target, damage=80, speed=200)
        self.color = (60, 60, 60)
        self.all_enemies = all_enemies
        self.splash_radius = 60

    def _on_hit(self):
        # Poškodí všechny nepřátele v okruhu
        hx, hy = self.center
        for enemy in self.all_enemies:
            if not enemy.alive:
                continue
            ex, ey = enemy.center
            if math.hypot(ex - hx, ey - hy) <= self.splash_radius:
                enemy.take_damage(self.damage)

    def draw(self, surface):
        cx, cy = int(self.x + 4), int(self.y + 4)
        pygame.draw.circle(surface, (80, 80, 80), (cx, cy), 7)
        pygame.draw.circle(surface, (140, 140, 140), (cx - 2, cy - 2), 3)


class FreezeBlast(Projectile):
    """Mrazivá střela – nízké poškození, ale zpomalí cíl."""
    def __init__(self, x, y, target):
        super().__init__(x, y, target, damage=10, speed=280)
        self.color = (100, 200, 255)

    def _on_hit(self):
        if self.target and self.target.alive:
            self.target.take_damage(self.damage)
            self.target.slow_timer = 2.5  # zpomalí na 2.5 sekundy

    def draw(self, surface):
        cx, cy = int(self.x + 4), int(self.y + 4)
        pygame.draw.circle(surface, (180, 230, 255), (cx, cy), 5)
        pygame.draw.circle(surface, (100, 200, 255), (cx, cy), 5, 1)
        # Malé hvězdičky okolo
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            sx = cx + int(math.cos(rad) * 8)
            sy = cy + int(math.sin(rad) * 8)
            pygame.draw.circle(surface, (200, 240, 255), (sx, sy), 2)