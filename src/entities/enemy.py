import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pygame
import math
from entities.base_entity import Entity
 
 
class Enemy(Entity):
    """
    Základní třída pro všechny nepřátele.
    Dědí od Entity, přidává pohyb po cestě, HP a odměnu.
    """
 
    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, 32, 32)
        self.path = path          # seznam bodů [(x,y), ...]
        self.path_index = 0
        self.speed = 80           # px/s – přepsáno v potomcích
        self.max_hp = 100
        self.hp = self.max_hp
        self.reward = 10          # zlato za zabití
        self.skin = skin
        self.slow_timer = 0.0    # sekundy zpomalení (FreezeBlast)
        self.color = (200, 50, 50)  # přepsáno v potomcích
        self.image = pygame.image.load("assets/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
 
    # ------------------------------------------------------------------
    # Pohyb po cestě
    # ------------------------------------------------------------------
    def update(self, dt: float):
        if self.slow_timer > 0:
            self.slow_timer -= dt
            effective_speed = self.speed * 0.4
        else:
            effective_speed = self.speed
 
        if self.path_index >= len(self.path):
            self.destroy()
            return
 
        target = self.path[self.path_index]
        tx, ty = target
        cx, cy = self.center
 
        dx = tx - cx
        dy = ty - cy
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
        # Tělo nepřítele
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
 
        # HP bar
        bar_w = self.width
        bar_h = 5
        bar_x = int(self.x)
        bar_y = int(self.y) - 8
        ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (80, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, (0, 220, 80), (bar_x, bar_y, int(bar_w * ratio), bar_h))
 
        # Rámeček při zpomalení
        if self.slow_timer > 0:
            pygame.draw.rect(surface, (100, 200, 255), self.rect, 2, border_radius=6)
 
    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp <= 0:
            self.destroy()
 
    @property
    def reached_end(self):
        return self.path_index >= len(self.path)
 
 
# ======================================================================
# 5 druhů nepřátel  (dědičnost + polymorfismus)
# ======================================================================
 
class BasicEnemy(Enemy):
    """Obyčejný nepřítel – vyvážené statistiky."""
    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, path, skin)
        self.speed = 80
        self.max_hp = 100
        self.hp = self.max_hp
        self.reward = 10
        self.color = (220, 60, 60)
 
    def draw(self, surface):
        super().draw(surface)
        # Čtverec v těle jako rozlišovací znak
        inner = pygame.Rect(int(self.x) + 8, int(self.y) + 8, 16, 16)
        pygame.draw.rect(surface, (255, 120, 120), inner, border_radius=3)
 
 
class FastEnemy(Enemy):
    """Rychlý, ale křehký nepřítel."""
    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, path, skin)
        self.speed = 160
        self.max_hp = 50
        self.hp = self.max_hp
        self.reward = 15
        self.width = 24
        self.height = 24
        self.color = (255, 200, 0)
 
    def draw(self, surface):
        # Trojúhelník jako tělo (rychlost)
        cx, cy = int(self.x + self.width // 2), int(self.y + self.height // 2)
        pts = [(cx, cy - 14), (cx - 12, cy + 10), (cx + 12, cy + 10)]
        pygame.draw.polygon(surface, self.color, pts)
        pygame.draw.polygon(surface, (200, 150, 0), pts, 2)
        # HP bar
        bar_w = self.width
        bar_x = int(self.x)
        bar_y = int(self.y) - 8
        ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (80, 0, 0), (bar_x, bar_y, bar_w, 5))
        pygame.draw.rect(surface, (0, 220, 80), (bar_x, bar_y, int(bar_w * ratio), 5))
        if self.slow_timer > 0:
            pygame.draw.polygon(surface, (100, 200, 255), pts, 3)
 
 
class TankEnemy(Enemy):
    """Pomalý tank s obrovským množstvím HP."""
    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, path, skin)
        self.speed = 40
        self.max_hp = 400
        self.hp = self.max_hp
        self.reward = 30
        self.width = 44
        self.height = 44
        self.color = (80, 80, 200)
 
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        # Vnitřní tmavý čtverec
        inner = pygame.Rect(int(self.x) + 6, int(self.y) + 6, 32, 32)
        pygame.draw.rect(surface, (50, 50, 150), inner, border_radius=3)
        # HP bar
        bar_w = self.width
        bar_x = int(self.x)
        bar_y = int(self.y) - 8
        ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (80, 0, 0), (bar_x, bar_y, bar_w, 6))
        pygame.draw.rect(surface, (0, 220, 80), (bar_x, bar_y, int(bar_w * ratio), 6))
        if self.slow_timer > 0:
            pygame.draw.rect(surface, (100, 200, 255), self.rect, 3, border_radius=4)
 
 
class FlyingEnemy(Enemy):
    """Létající nepřítel – ignoruje zem, létá sinusoidálně."""
    def __init__(self, x, y, path, skin="default"):
        super().__init__(x, y, path, skin)
        self.speed = 110
        self.max_hp = 70
        self.hp = self.max_hp
        self.reward = 20
        self.color = (150, 50, 220)
        self.fly_offset = 0.0
        self.fly_time = 0.0

    def update(self, dt):
        self.fly_time += dt
        super().update(dt)

    # 👇 MUSÍ být tady (odsazení!)
    def draw(self, surface):
        visual_y = self.y + math.sin(self.fly_time * 4) * 6

        # PNG
        surface.blit(self.image, (int(self.x), int(visual_y)))

        # HP bar
        bar_w = self.width
        bar_x = int(self.x)
        bar_y = int(visual_y) - 8
        ratio = max(0, self.hp / self.max_hp)

        pygame.draw.rect(surface, (80, 0, 0), (bar_x, bar_y, bar_w, 5))
        pygame.draw.rect(surface, (0, 220, 80), (bar_x, bar_y, int(bar_w * ratio), 5))
 
 
class BossEnemy(Enemy):
    """Boss – obrovský, rychle se regeneruje, velká odměna."""
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
 
    def update(self, dt):
        # Regenerace HP každé 2 sekundy
        self.regen_timer += dt
        if self.regen_timer >= 2.0:
            self.regen_timer = 0.0
            self.hp = min(self.max_hp, self.hp + 20)
        super().update(dt)
 
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        # Korunka
        crown_pts = [
            (int(self.x) + 4, int(self.y) + 4),
            (int(self.x) + 4, int(self.y) - 10),
            (int(self.x) + 16, int(self.y) + 2),
            (int(self.x) + 28, int(self.y) - 10),
            (int(self.x) + 40, int(self.y) + 2),
            (int(self.x) + 52, int(self.y) - 10),
            (int(self.x) + 52, int(self.y) + 4),
        ]
        pygame.draw.lines(surface, (255, 215, 0), False, crown_pts, 3)
        # Oči
        eye_y = int(self.y) + 18
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x) + 16, eye_y), 7)
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x) + 40, eye_y), 7)
        pygame.draw.circle(surface, (0, 0, 0), (int(self.x) + 16, eye_y), 3)
        pygame.draw.circle(surface, (0, 0, 0), (int(self.x) + 40, eye_y), 3)
        # HP bar
        bar_w = self.width
        bar_x = int(self.x)
        bar_y = int(self.y) - 14
        ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (80, 0, 0), (bar_x, bar_y, bar_w, 7))
        pygame.draw.rect(surface, (255, 50, 50), (bar_x, bar_y, int(bar_w * ratio), 7))
        if self.slow_timer > 0:
            pygame.draw.rect(surface, (100, 200, 255), self.rect, 3, border_radius=8)