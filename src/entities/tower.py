import pygame
import math
from src.entities.base_entity import Entity
from src.entities.projectile import Arrow, Cannonball, FreezeBlast


class Tower(Entity):
    """Třída pro všechny věže. Dědí od Entity, přidává střílení na nepřátele."""

    def __init__(self, x, y, cell_size=64):
        super().__init__(x, y, cell_size, cell_size)
        self.range = 150   
        self.fire_rate = 1.0   
        self.fire_timer = 0.0
        self.cost = 100
        self.level = 1
        self.color = (100, 180, 100)
        self.name = "Věž"

    def update(self, dt: float, enemies: list, projectiles: list):
        self.fire_timer += dt
        if self.fire_timer >= 1.0 / self.fire_rate:
            target = self._find_target(enemies)
            if target:
                self._shoot(target, enemies, projectiles)
                self.fire_timer = 0.0

    def _find_target(self, enemies):
        best = None
        best_idx = -1
        cx, cy = self.center
        for enemy in enemies:
            if not enemy.alive:
                continue
            ex, ey = enemy.center
            dist = math.hypot(ex - cx, ey - cy)
            if dist <= self.range and enemy.path_index > best_idx:
                best = enemy
                best_idx = enemy.path_index
        return best

    def _shoot(self, target, enemies, projectiles):
        """Přepsáno v potomcích – polymorfismus."""
        raise NotImplementedError

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)

    def draw_range(self, surface: pygame.Surface):
        cx, cy = self.center
        range_surf = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(range_surf, (255, 255, 255, 30), (self.range, self.range), self.range)
        pygame.draw.circle(range_surf, (255, 255, 255, 80), (self.range, self.range), self.range, 1)
        surface.blit(range_surf, (cx - self.range, cy - self.range))

    def upgrade(self):
        self.level += 1

    def get_upgrade_cost(self):
        return self.cost * self.level


class ArrowTower(Tower):
    """Lučištník – rychlá střelba, nízké poškození."""

    def __init__(self, x, y, cell_size=64):
        super().__init__(x, y, cell_size)
        self.range = 160
        self.fire_rate = 1.8
        self.cost = 80
        self.color = (60, 160, 60)
        self.name = "Lučištník"

    def _shoot(self, target, enemies, projectiles):
        cx, cy = self.center
        projectiles.append(Arrow(cx - 4, cy - 4, target))

    def draw(self, surface):
        super().draw(surface)
        cx, cy = self.center
    
        pygame.draw.arc(surface, (180, 120, 40),
                        (cx - 14, cy - 14, 28, 28), 0.5, 2.6, 3)
        pygame.draw.line(surface, (180, 120, 40), (cx - 8, cy), (cx + 12, cy), 2)

    def upgrade(self):
        super().upgrade()
        self.fire_rate += 0.4
        self.range += 15


class CannonTower(Tower):
    """Dělo – pomalá střelba, velké poškození + splash."""

    def __init__(self, x, y, cell_size=64):
        super().__init__(x, y, cell_size)
        self.range = 130
        self.fire_rate = 0.6
        self.cost = 150
        self.color = (80, 80, 160)
        self.name = "Dělo"

    def _shoot(self, target, enemies, projectiles):
        cx, cy = self.center
        projectiles.append(Cannonball(cx - 4, cy - 4, target, enemies))

    def draw(self, surface):
        super().draw(surface)
        cx, cy = self.center
        pygame.draw.circle(surface, (50, 50, 120), (cx, cy), 18)
        pygame.draw.circle(surface, (100, 100, 200), (cx, cy), 18, 2)
        pygame.draw.rect(surface, (40, 40, 100), (cx - 4, cy - 20, 8, 20), border_radius=3)

    def upgrade(self):
        super().upgrade()
        self.range += 10


class FreezeTower(Tower):
    """Mrazivá věž – zpomaluje nepřátele."""
    def __init__(self, x, y, cell_size=64):
        super().__init__(x, y, cell_size)
        self.range = 120
        self.fire_rate = 0.9
        self.cost = 120
        self.color = (60, 180, 220)
        self.name = "Mrazič"

    def _shoot(self, target, enemies, projectiles):
        cx, cy = self.center
        projectiles.append(FreezeBlast(cx - 4, cy - 4, target))

    def draw(self, surface):
        super().draw(surface)
        cx, cy = self.center
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            ex = cx + int(math.cos(rad) * 18)
            ey = cy + int(math.sin(rad) * 18)
            pygame.draw.line(surface, (200, 240, 255), (cx, cy), (ex, ey), 2)
        pygame.draw.circle(surface, (240, 250, 255), (cx, cy), 6)

    def upgrade(self):
        super().upgrade()
        self.fire_rate += 0.3
        self.range += 20