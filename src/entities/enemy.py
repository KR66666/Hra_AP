import pygame
import math
import os
from src.entities.base_entity import Entity


def _load_image(filename: str, size: tuple) -> pygame.Surface | None:
    """
    Načte obrázek ze složky assets/.
    Pokud soubor neexistuje, vrátí None a použije se fallback kreslení.
    """
    path = os.path.join("assets", filename)
    if not os.path.exists(path):
        return None
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except pygame.error:
        return None


class Enemy(Entity):
    """
    Základní třída pro všechny nepřátele.
    Pokud existuje obrázek v assets/, použije ho.
    Jinak kreslí fallback tvary.
    """

    IMAGE_FILE = "enemy.png"   # přepsáno v potomcích

    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, 32, 32)
        self.path = path
        self.path_index = 0
        self.speed = 80
        self.max_hp = 100
        self.hp = self.max_hp
        self.reward = 10
        self.skin = skin
        self.slow_timer = 0.0
        self.color = (200, 50, 50)   # fallback barva
        self._anim_t = 0.0

        # Načti obrázek (sdílený cache na třídě, aby se nenahrával opakovaně)
        cache_key = (self.__class__.__name__, self.width, self.height)
        if not hasattr(Enemy, "_img_cache"):
            Enemy._img_cache = {}
        if cache_key not in Enemy._img_cache:
            Enemy._img_cache[cache_key] = _load_image(self.IMAGE_FILE, (self.width, self.height))
        self._image = Enemy._img_cache[cache_key]

    # ------------------------------------------------------------------
    # Pohyb po cestě
    # ------------------------------------------------------------------
    def update(self, dt: float):
        self._anim_t += dt
        if self.slow_timer > 0:
            self.slow_timer -= dt
            effective_speed = self.speed * 0.4
        else:
            effective_speed = self.speed

        if self.path_index >= len(self.path):
            self.destroy()
            return

        tx, ty = self.path[self.path_index]
        cx, cy = self.center
        dx, dy = tx - cx, ty - cy
        dist = math.hypot(dx, dy)
        if dist < 4:
            self.path_index += 1
        else:
            move = effective_speed * dt
            self.x += (dx / dist) * move
            self.y += (dy / dist) * move

    # ------------------------------------------------------------------
    # Kreslení
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface):
        if self._image:
            surface.blit(self._image, (int(self.x), int(self.y)))
        else:
            self._draw_fallback(surface)

        self._draw_hp_bar(surface)
        self._draw_slow_ring(surface)

    def _draw_fallback(self, surface):
        """Záložní kreslení pokud obrázek chybí."""
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)

    def _draw_hp_bar(self, surface):
        bar_x = int(self.x)
        bar_y = int(self.y) - 8
        bar_w = self.width
        ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (60, 0, 0), (bar_x, bar_y, bar_w, 5), border_radius=2)
        if ratio > 0:
            bar_color = (int(255 * (1 - ratio)), int(200 * ratio), 40)
            pygame.draw.rect(surface, bar_color,
                             (bar_x, bar_y, int(bar_w * ratio), 5), border_radius=2)

    def _draw_slow_ring(self, surface):
        if self.slow_timer > 0:
            pulse = abs(math.sin(self._anim_t * 6)) * 40
            color = (80, int(180 + pulse), 255)
            pygame.draw.rect(surface, color, self.rect, 2, border_radius=6)

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp <= 0:
            self.destroy()

    @property
    def reached_end(self):
        return self.path_index >= len(self.path)


# ======================================================================
# 5 druhů nepřátel – každý má vlastní IMAGE_FILE a fallback barvu
# ======================================================================

class BasicEnemy(Enemy):
    """Obyčejný nepřítel. Obrázek: assets/basic_enemy.png"""
    IMAGE_FILE = "basic_enemy.png"

    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, path, skin)
        self.speed = 80
        self.max_hp = 100
        self.hp = self.max_hp
        self.reward = 10
        self.color = (220, 60, 60)

    def _draw_fallback(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
        inner = pygame.Rect(int(self.x) + 8, int(self.y) + 8, 16, 16)
        pygame.draw.rect(surface, (255, 120, 120), inner, border_radius=3)


class FastEnemy(Enemy):
    """Rychlý nepřítel. Obrázek: assets/fast_enemy.png"""
    IMAGE_FILE = "fast_enemy.png"

    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, path, skin)
        self.speed = 165
        self.max_hp = 50
        self.hp = self.max_hp
        self.reward = 15
        self.width = 24
        self.height = 24
        self.color = (255, 200, 0)
        # Znovu načti obrázek ve správné velikosti
        cache_key = (self.__class__.__name__, self.width, self.height)
        if cache_key not in Enemy._img_cache:
            Enemy._img_cache[cache_key] = _load_image(self.IMAGE_FILE, (self.width, self.height))
        self._image = Enemy._img_cache[cache_key]

    def _draw_fallback(self, surface):
        cx = int(self.x + self.width // 2)
        cy = int(self.y + self.height // 2)
        pts = [(cx, cy - 14), (cx - 12, cy + 10), (cx + 12, cy + 10)]
        pygame.draw.polygon(surface, self.color, pts)
        pygame.draw.polygon(surface, (200, 150, 0), pts, 2)


class TankEnemy(Enemy):
    """Tankový nepřítel. Obrázek: assets/tank_enemy.png"""
    IMAGE_FILE = "tank_enemy.png"

    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, path, skin)
        self.speed = 40
        self.max_hp = 400
        self.hp = self.max_hp
        self.reward = 30
        self.width = 44
        self.height = 44
        self.color = (80, 80, 200)
        cache_key = (self.__class__.__name__, self.width, self.height)
        if cache_key not in Enemy._img_cache:
            Enemy._img_cache[cache_key] = _load_image(self.IMAGE_FILE, (self.width, self.height))
        self._image = Enemy._img_cache[cache_key]

    def _draw_fallback(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        inner = pygame.Rect(int(self.x) + 6, int(self.y) + 6, 32, 32)
        pygame.draw.rect(surface, (50, 50, 150), inner, border_radius=3)


class FlyingEnemy(Enemy):
    """Létající nepřítel. Obrázek: assets/flying_enemy.png"""
    IMAGE_FILE = "flying_enemy.png"

    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, path, skin)
        self.speed = 115
        self.max_hp = 70
        self.hp = self.max_hp
        self.reward = 20
        self.color = (150, 50, 220)

    def update(self, dt):
        super().update(dt)

    def draw(self, surface):
        # Létající offset – sinusoidální pohyb
        fly_off = math.sin(self._anim_t * 5) * 6
        orig_y = self.y
        self.y += fly_off

        if self._image:
            surface.blit(self._image, (int(self.x), int(self.y)))
        else:
            self._draw_fallback(surface)

        self._draw_hp_bar(surface)
        self._draw_slow_ring(surface)
        self.y = orig_y  # vrať zpět

    def _draw_fallback(self, surface):
        rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        pygame.draw.ellipse(surface, self.color, rect)
        pygame.draw.ellipse(surface, (200, 100, 255), rect, 2)


class BossEnemy(Enemy):
    """Boss nepřítel. Obrázek: assets/boss_enemy.png"""
    IMAGE_FILE = "boss_enemy.png"

    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, path, skin)
        self.speed = 55
        self.max_hp = 1200
        self.hp = self.max_hp
        self.reward = 150
        self.width = 56
        self.height = 56
        self.color = (180, 20, 20)
        self.regen_timer = 0.0
        cache_key = (self.__class__.__name__, self.width, self.height)
        if cache_key not in Enemy._img_cache:
            Enemy._img_cache[cache_key] = _load_image(self.IMAGE_FILE, (self.width, self.height))
        self._image = Enemy._img_cache[cache_key]

    def update(self, dt):
        self.regen_timer += dt
        if self.regen_timer >= 2.0:
            self.regen_timer = 0.0
            self.hp = min(self.max_hp, self.hp + 20)
        super().update(dt)

    def _draw_fallback(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        # Korunka
        crown_pts = [
            (int(self.x) + 4,  int(self.y) + 4),
            (int(self.x) + 4,  int(self.y) - 10),
            (int(self.x) + 16, int(self.y) + 2),
            (int(self.x) + 28, int(self.y) - 10),
            (int(self.x) + 40, int(self.y) + 2),
            (int(self.x) + 52, int(self.y) - 10),
            (int(self.x) + 52, int(self.y) + 4),
        ]
        pygame.draw.lines(surface, (255, 215, 0), False, crown_pts, 3)
        # Oči
        eye_y = int(self.y) + 20
        for ex in [int(self.x) + 16, int(self.x) + 40]:
            pygame.draw.circle(surface, (255, 255, 0), (ex, eye_y), 7)
            pygame.draw.circle(surface, (0, 0, 0), (ex, eye_y), 3)