import pygame
import math
import random


class Effect:
    """Základní třída pro všechny vizuální efekty."""

    def __init__(self, x: float, y: float, duration: float):
        self.x = x
        self.y = y
        self.duration = duration
        self.timer = 0.0
        self.alive = True

    @property
    def progress(self) -> float:
        return min(1.0, self.timer / self.duration)

    def update(self, dt: float):
        self.timer += dt
        if self.timer >= self.duration:
            self.alive = False

    def draw(self, surface: pygame.Surface):
        raise NotImplementedError


class Particle(Effect):
    def __init__(self, x, y, color, angle, speed, size=4, duration=0.6):
        super().__init__(x, y, duration)
        self.color = color
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.size = size
        self.gravity = 120

    def update(self, dt):
        super().update(dt)
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt

    def draw(self, surface):
        alpha = int(255 * (1.0 - self.progress))
        size = max(1, int(self.size * (1.0 - self.progress * 0.5)))
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        r, g, b = self.color[:3]
        pygame.draw.circle(surf, (r, g, b, alpha), (size, size), size)
        surface.blit(surf, (int(self.x) - size, int(self.y) - size))


class Explosion(Effect):
    def __init__(self, x, y, radius=40, color=(255, 150, 50), duration=0.4):
        super().__init__(x, y, duration)
        self.max_radius = radius
        self.color = color

    def draw(self, surface):
        r = int(self.max_radius * self.progress)
        alpha = int(200 * (1.0 - self.progress))
        if r <= 0:
            return
        surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
        col = (*self.color[:3], alpha)
        pygame.draw.circle(surf, col, (r + 2, r + 2), r, max(1, int(4 * (1 - self.progress))))
        surface.blit(surf, (int(self.x) - r - 2, int(self.y) - r - 2))


class FreezeRing(Effect):
    def __init__(self, x, y, duration=0.5):
        super().__init__(x, y, duration)

    def draw(self, surface):
        r = int(30 * self.progress)
        alpha = int(180 * (1.0 - self.progress))
        if r <= 0:
            return
        surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(surf, (100, 200, 255, alpha), (r + 2, r + 2), r, 3)
        surface.blit(surf, (int(self.x) - r - 2, int(self.y) - r - 2))


class FloatingText(Effect):
    def __init__(self, x, y, text: str, color=(255, 220, 50), font_size=20, duration=1.2):
        super().__init__(x, y, duration)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.rise_speed = 40

    def update(self, dt):
        super().update(dt)
        self.y -= self.rise_speed * dt

    def draw(self, surface):
        alpha = int(255 * (1.0 - self.progress ** 2))
        surf = self.font.render(self.text, True, self.color)
        surf.set_alpha(alpha)
        surface.blit(surf, (int(self.x) - surf.get_width() // 2, int(self.y)))


class LightningBolt(Effect):
    def __init__(self, x1, y1, x2, y2, color=(180, 100, 255), duration=0.15):
        super().__init__(x1, y1, duration)
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.points = self._gen_points(x1, y1, x2, y2)

    def _gen_points(self, x1, y1, x2, y2, segments=8):
        pts = [(x1, y1)]
        for i in range(1, segments):
            t = i / segments
            mx = x1 + (x2 - x1) * t + random.uniform(-12, 12)
            my = y1 + (y2 - y1) * t + random.uniform(-12, 12)
            pts.append((mx, my))
        pts.append((x2, y2))
        return pts

    def draw(self, surface):
        alpha = int(255 * (1.0 - self.progress))
        width = max(1, int(3 * (1.0 - self.progress)))
        if len(self.points) < 2:
            return
        surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        r, g, b = self.color[:3]
        pygame.draw.lines(surf, (r, g, b, alpha), False,
                          [(int(p[0]), int(p[1])) for p in self.points], width)
        pygame.draw.lines(surf, (220, 200, 255, min(255, alpha + 60)), False,
                          [(int(p[0]), int(p[1])) for p in self.points], max(1, width - 1))
        surface.blit(surf, (0, 0))


class EffectManager:
    def __init__(self):
        self._effects: list[Effect] = []

    def add(self, effect: Effect):
        self._effects.append(effect)

    def spawn_explosion(self, x, y, color=(255, 150, 50), radius=40, n_particles=12):
        self.add(Explosion(x, y, radius, color))
        for _ in range(n_particles):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(60, 160)
            size  = random.randint(3, 7)
            dur   = random.uniform(0.4, 0.8)
            self.add(Particle(x, y, color, angle, speed, size, dur))

    def spawn_freeze(self, x, y):
        self.add(FreezeRing(x, y))
        for _ in range(8):
            angle = random.uniform(0, math.pi * 2)
            self.add(Particle(x, y, (150, 220, 255), angle,
                              random.uniform(40, 100), 3, 0.5))

    def spawn_gold(self, x, y, amount: int):
        self.add(FloatingText(x, y, f"+{amount}⬡", (255, 220, 50)))

    def spawn_damage(self, x, y, amount: int):
        self.add(FloatingText(x, y, f"-{amount}", (255, 80, 80), font_size=16, duration=0.8))

    def spawn_lightning(self, x1, y1, x2, y2):
        self.add(LightningBolt(x1, y1, x2, y2))

    def spawn_place(self, x, y):
        for _ in range(16):
            angle = random.uniform(0, math.pi * 2)
            self.add(Particle(x, y, (100, 255, 120), angle,
                              random.uniform(50, 120), 4, 0.5))

    def update(self, dt: float):
        for e in self._effects:
            e.update(dt)
        self._effects = [e for e in self._effects if e.alive]

    def draw(self, surface: pygame.Surface):
        for e in self._effects:
            e.draw(surface)