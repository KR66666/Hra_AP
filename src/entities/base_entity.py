import pygame


class Entity:
    """
    Základní třída pro všechny herní objekty.
    Od této třídy dědí Enemy, Tower i Projectile.
    """

    def __init__(self, x: float, y: float, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    @property
    def center(self) -> tuple:
        return (self.x + self.width // 2, self.y + self.height // 2)

    def update(self, dt: float):
        """Přepsáno v každé podtřídě – polymorfismus."""
        raise NotImplementedError

    def draw(self, surface: pygame.Surface):
        """Přepsáno v každé podtřídě – polymorfismus."""
        raise NotImplementedError

    def destroy(self):
        self.alive = False