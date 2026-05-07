import pygame
from src.level import ALL_LEVELS


class Menu:
    """
    Hlavní menu hry.
    """

    def __init__(self, screen_w, screen_h, font):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.title_font = pygame.font.SysFont("Arial", 52, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18)

        cx = screen_w // 2
        self.btn_play     = pygame.Rect(cx - 110, 260, 220, 55)
        self.btn_settings = pygame.Rect(cx - 110, 330, 220, 55)
        self.btn_quit     = pygame.Rect(cx - 110, 400, 220, 55)

        self.action = None  # "play" | "settings" | "quit"

    def handle_event(self, event):
        self.action = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_play.collidepoint(event.pos):
                self.action = "play"
            elif self.btn_settings.collidepoint(event.pos):
                self.action = "settings"
            elif self.btn_quit.collidepoint(event.pos):
                self.action = "quit"

    def draw(self, surface):
        surface.fill((15, 25, 15))

        # Pozadí – dekorativní čáry
        for i in range(0, self.screen_w, 60):
            pygame.draw.line(surface, (25, 40, 25), (i, 0), (i, self.screen_h), 1)
        for j in range(0, self.screen_h, 60):
            pygame.draw.line(surface, (25, 40, 25), (0, j), (self.screen_w, j), 1)

        # Titulek
        title = self.title_font.render("Tower Defense", True, (255,192,203))
        sub   = self.small_font.render("Bráň svou základnu!", True, (140, 200, 140))
        surface.blit(title, (self.screen_w // 2 - title.get_width() // 2, 120))
        surface.blit(sub,   (self.screen_w // 2 - sub.get_width() // 2,   185))

        self._draw_btn(surface, self.btn_play,     "▶  Hrát")
        self._draw_btn(surface, self.btn_settings, "⚙  Nastavení")
        self._draw_btn(surface, self.btn_quit,     "✕  Konec")

        ver = self.small_font.render("v1.0", True, (60, 80, 60))
        surface.blit(ver, (self.screen_w - 50, self.screen_h - 25))

    def _draw_btn(self, surface, rect, label):
        hover = rect.collidepoint(pygame.mouse.get_pos())
        bg    = (50, 120, 50) if hover else (30, 70, 30)
        border= (120, 220, 120) if hover else (60, 100, 60)
        pygame.draw.rect(surface, bg, rect, border_radius=10)
        pygame.draw.rect(surface, border, rect, 2, border_radius=10)
        txt = self.font.render(label, True, (230, 255, 230))
        surface.blit(txt, (rect.x + rect.w // 2 - txt.get_width() // 2,
                           rect.y + rect.h // 2 - txt.get_height() // 2))


class PauseMenu:
    """
    Pauza – zobrazuje se přes herní plochu.
    """

    def __init__(self, screen_w, screen_h, font):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)

        cx = screen_w // 2
        cy = screen_h // 2
        self.btn_resume   = pygame.Rect(cx - 100, cy - 60, 200, 50)
        self.btn_settings = pygame.Rect(cx - 100, cy + 10,  200, 50)
        self.btn_menu     = pygame.Rect(cx - 100, cy + 80,  200, 50)

        self.action = None  # "resume" | "settings" | "menu"

    def handle_event(self, event):
        self.action = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_resume.collidepoint(event.pos):
                self.action = "resume"
            elif self.btn_settings.collidepoint(event.pos):
                self.action = "settings"
            elif self.btn_menu.collidepoint(event.pos):
                self.action = "menu"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.action = "resume"

    def draw(self, surface):
        # Tmavý overlay
        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        # Karta
        card = pygame.Rect(self.screen_w // 2 - 130, self.screen_h // 2 - 130, 260, 280)
        pygame.draw.rect(surface, (25, 35, 25), card, border_radius=14)
        pygame.draw.rect(surface, (80, 160, 80), card, 2, border_radius=14)

        title = self.title_font.render("Pauza", True, (180, 255, 180))
        surface.blit(title, (self.screen_w // 2 - title.get_width() // 2,
                              self.screen_h // 2 - 120))

        self._draw_btn(surface, self.btn_resume,   "▶  Pokračovat")
        self._draw_btn(surface, self.btn_settings, "⚙  Nastavení")
        self._draw_btn(surface, self.btn_menu,     "⌂  Hlavní menu")

    def _draw_btn(self, surface, rect, label):
        hover = rect.collidepoint(pygame.mouse.get_pos())
        bg    = (50, 110, 50) if hover else (30, 65, 30)
        border= (120, 200, 120) if hover else (55, 90, 55)
        pygame.draw.rect(surface, bg, rect, border_radius=8)
        pygame.draw.rect(surface, border, rect, 2, border_radius=8)
        txt = self.font.render(label, True, (230, 255, 230))
        surface.blit(txt, (rect.x + rect.w // 2 - txt.get_width() // 2,
                           rect.y + rect.h // 2 - txt.get_height() // 2))


class SettingsMenu:
    """
    Nastavení – hlasitost, FPS limit.
    """

    def __init__(self, screen_w, screen_h, font, settings: dict):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.settings = settings  # sdílený dict se zbytkem hry
        self.action = None  # "back"

        cx = screen_w // 2
        self.vol_minus = pygame.Rect(cx - 120, 280, 40, 40)
        self.vol_plus  = pygame.Rect(cx + 80,  280, 40, 40)
        self.fps_minus = pygame.Rect(cx - 120, 360, 40, 40)
        self.fps_plus  = pygame.Rect(cx + 80,  360, 40, 40)
        self.btn_back  = pygame.Rect(cx - 100, 440, 200, 50)

    def handle_event(self, event):
        self.action = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.vol_minus.collidepoint(event.pos):
                self.settings["volume"] = max(0, self.settings["volume"] - 10)
            if self.vol_plus.collidepoint(event.pos):
                self.settings["volume"] = min(100, self.settings["volume"] + 10)
            if self.fps_minus.collidepoint(event.pos):
                self.settings["fps"] = max(30, self.settings["fps"] - 15)
            if self.fps_plus.collidepoint(event.pos):
                self.settings["fps"] = min(120, self.settings["fps"] + 15)
            if self.btn_back.collidepoint(event.pos):
                self.action = "back"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.action = "back"

    def draw(self, surface):
        surface.fill((15, 20, 30))

        title = self.title_font.render("Nastavení", True, (180, 200, 255))
        surface.blit(title, (self.screen_w // 2 - title.get_width() // 2, 100))

        self._draw_setting(surface, "Hlasitost", self.settings["volume"],
                           self.vol_minus, self.vol_plus, 280, suffix="%")
        self._draw_setting(surface, "FPS limit", self.settings["fps"],
                           self.fps_minus, self.fps_plus, 360)

        # Tlačítko zpět
        hover = self.btn_back.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, (50, 80, 120) if hover else (30, 50, 80), self.btn_back, border_radius=8)
        pygame.draw.rect(surface, (100, 140, 220), self.btn_back, 2, border_radius=8)
        bt = self.font.render("← Zpět", True, (200, 220, 255))
        surface.blit(bt, (self.btn_back.x + self.btn_back.w // 2 - bt.get_width() // 2,
                          self.btn_back.y + 12))

    def _draw_setting(self, surface, label, value, btn_minus, btn_plus, y, suffix=""):
        cx = self.screen_w // 2
        lbl = self.font.render(label, True, (200, 200, 220))
        surface.blit(lbl, (cx - lbl.get_width() // 2, y - 30))

        for btn, sym in [(btn_minus, "−"), (btn_plus, "+")]:
            hover = btn.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(surface, (60, 80, 100) if hover else (40, 55, 70), btn, border_radius=6)
            pygame.draw.rect(surface, (120, 160, 200), btn, 2, border_radius=6)
            s = self.font.render(sym, True, (220, 240, 255))
            surface.blit(s, (btn.x + btn.w // 2 - s.get_width() // 2,
                             btn.y + btn.h // 2 - s.get_height() // 2))

        val_txt = self.font.render(f"{value}{suffix}", True, (255, 255, 180))
        surface.blit(val_txt, (cx - val_txt.get_width() // 2, y + 2))


class GameOverScreen:
    """Obrazovka konce hry (prohra nebo výhra)."""

    def __init__(self, screen_w, screen_h, font, won: bool, has_next_level: bool = False):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.title_font = pygame.font.SysFont("Arial", 52, bold=True)
        self.won = won
        self.has_next_level = has_next_level  # ← NOVÉ: je další level?
        self.action = None  # "menu" | "restart" | "next"

        cx = screen_w // 2
        cy = screen_h // 2

        if won and has_next_level:
            # 3 tlačítka: Další level, Znovu, Menu
            self.btn_next    = pygame.Rect(cx - 110, cy - 80, 220, 55)
            self.btn_restart = pygame.Rect(cx - 110, cy - 10, 220, 55)
            self.btn_menu    = pygame.Rect(cx - 110, cy + 60, 220, 55)
        else:
            # 2 tlačítka: Znovu, Menu
            self.btn_next    = None
            self.btn_restart = pygame.Rect(cx - 110, cy - 10, 220, 55)
            self.btn_menu    = pygame.Rect(cx - 110, cy + 60, 220, 55)

    def handle_event(self, event):
        self.action = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_next and self.btn_next.collidepoint(event.pos):
                self.action = "next"
            elif self.btn_restart.collidepoint(event.pos):
                self.action = "restart"
            elif self.btn_menu.collidepoint(event.pos):
                self.action = "menu"

    def draw(self, surface):
        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        color = (100, 255, 100) if self.won else (255, 80, 80)
        label = "Výhra! 🏆" if self.won else "Prohra! 💀"
        title = self.title_font.render(label, True, color)
        surface.blit(title, (self.screen_w // 2 - title.get_width() // 2,
                              self.screen_h // 2 - 150))

        # Tlačítko Další level (jen při výhře s dalším levelem)
        if self.btn_next:
            self._draw_btn(surface, self.btn_next, "▶▶  Další level",
                           hover_color=(50, 150, 50), base_color=(30, 100, 30),
                           border_color=(100, 220, 100), text_color=(200, 255, 200))

        self._draw_btn(surface, self.btn_restart, "↺  Znovu")
        self._draw_btn(surface, self.btn_menu,    "⌂  Menu")

    def _draw_btn(self, surface, rect, label,
                  hover_color=(60, 60, 60), base_color=(35, 35, 35),
                  border_color=(150, 150, 150), text_color=(230, 230, 230)):
        hover = rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, hover_color if hover else base_color, rect, border_radius=10)
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=10)
        t = self.font.render(label, True, text_color)
        surface.blit(t, (rect.x + rect.w // 2 - t.get_width() // 2,
                         rect.y + rect.h // 2 - t.get_height() // 2))