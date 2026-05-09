import pygame
from src.level import ALL_LEVELS


# ---------------------------------------------------------------
# Barvy pro každý skin
# ---------------------------------------------------------------
SKIN_COLORS = {
    "default": {
        "menu_bg":        (240, 248, 230),
        "btn_bg":         (100, 60, 180),
        "btn_hover":      (140, 90, 220),
        "btn_border":     (70,  30, 140),
        "btn_hover_brd":  (170, 130, 255),
        "btn_text":       (240, 255, 240),
        "title":          (50,  20, 100),
        "sub":            (80,  50, 140),
        "pause_card_bg":  (230, 220, 255),
        "pause_card_brd": (140, 100, 220),
        "pause_title":    (70,  30, 150),
        "pause_btn_bg":   (120, 70, 200),
        "pause_btn_hov":  (160, 110, 240),
        "pause_btn_brd":  (80,  40, 160),
        "win_color":      (60,  180, 100),
        "lose_color":     (200,  50,  70),
        "over_btn_bg":    (100, 60, 180),
        "over_btn_hov":   (140, 90, 220),
        "over_btn_brd":   (180, 140, 255),
        "over_btn_txt":   (240, 230, 255),
        "next_btn_bg":    (60,  150,  80),
        "next_btn_hov":   (80,  200, 110),
        "next_btn_brd":   (120, 230, 150),
        "next_btn_txt":   (220, 255, 230),
    },
    "dark": {
        "menu_bg":        (12,  10,  20),
        "btn_bg":         (140,  40,  10),
        "btn_hover":      (200,  70,  20),
        "btn_border":     (80,   20,   5),
        "btn_hover_brd":  (240, 100,  40),
        "btn_text":       (255, 220, 200),
        "title":          (255, 160,  60),
        "sub":            (220, 120,  50),
        "pause_card_bg":  (25,  12,   8),
        "pause_card_brd": (180,  60,  20),
        "pause_title":    (255, 160,  60),
        "pause_btn_bg":   (140,  40,  10),
        "pause_btn_hov":  (200,  70,  20),
        "pause_btn_brd":  (200,  80,  30),
        "win_color":      (255, 160,  40),
        "lose_color":     (220,  50,  30),
        "over_btn_bg":    (140,  40,  10),
        "over_btn_hov":   (200,  70,  20),
        "over_btn_brd":   (220, 100,  40),
        "over_btn_txt":   (255, 220, 200),
        "next_btn_bg":    (100,  80,  10),
        "next_btn_hov":   (160, 130,  20),
        "next_btn_brd":   (220, 180,  40),
        "next_btn_txt":   (255, 240, 180),
    },
}


def get_c(skin, key):
    return SKIN_COLORS.get(skin, SKIN_COLORS["default"]).get(key, (128, 128, 128))


# ---------------------------------------------------------------
class Menu:
    """Hlavní menu hry."""

    def __init__(self, screen_w, screen_h, font, skin="default"):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.skin = skin
        self.title_font = pygame.font.SysFont("Arial", 52, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18)

        cx = 690
        self.btn_play     = pygame.Rect(cx - 110, 270, 220, 55)
        self.btn_settings = pygame.Rect(cx - 110, 340, 220, 55)
        self.btn_quit     = pygame.Rect(cx - 110, 410, 220, 55)
        self.action = None

        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (screen_w, screen_h))

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
        surface.blit(self.background, (0, 0))

        title = self.title_font.render("Tower Defense", True, get_c(self.skin, "title"))
        sub   = self.small_font.render("Bráň svou základnu!", True, get_c(self.skin, "sub"))
        surface.blit(title, (500, 120))
        surface.blit(sub,   (620, 190))

        self._draw_btn(surface, self.btn_play,     "Hrát")
        self._draw_btn(surface, self.btn_settings, "Nastavení")
        self._draw_btn(surface, self.btn_quit,     "Konec")

        ver = self.small_font.render("v1.0", True, (80, 80, 80))
        surface.blit(ver, (self.screen_w - 50, self.screen_h - 25))

    def _draw_btn(self, surface, rect, label):
        hover  = rect.collidepoint(pygame.mouse.get_pos())
        bg     = get_c(self.skin, "btn_hover")  if hover else get_c(self.skin, "btn_bg")
        border = get_c(self.skin, "btn_hover_brd") if hover else get_c(self.skin, "btn_border")
        pygame.draw.rect(surface, bg, rect, border_radius=10)
        pygame.draw.rect(surface, border, rect, 2, border_radius=10)
        txt = self.font.render(label, True, get_c(self.skin, "btn_text"))
        surface.blit(txt, (rect.x + rect.w // 2 - txt.get_width() // 2,
                           rect.y + rect.h // 2 - txt.get_height() // 2))


# ---------------------------------------------------------------
class PauseMenu:
    """Pauza – zobrazuje se přes herní plochu."""

    def __init__(self, screen_w, screen_h, font, skin="default"):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.skin = skin
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)

        cx = screen_w // 2
        cy = screen_h // 2
        self.btn_resume   = pygame.Rect(cx - 100, cy - 60, 200, 50)
        self.btn_settings = pygame.Rect(cx - 100, cy + 10,  200, 50)
        self.btn_menu     = pygame.Rect(cx - 100, cy + 80,  200, 50)
        self.action = None

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
        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        card = pygame.Rect(self.screen_w // 2 - 130, self.screen_h // 2 - 130, 260, 280)
        pygame.draw.rect(surface, get_c(self.skin, "pause_card_bg"),  card, border_radius=14)
        pygame.draw.rect(surface, get_c(self.skin, "pause_card_brd"), card, 2, border_radius=14)

        title = self.title_font.render("Pauza", True, get_c(self.skin, "pause_title"))
        surface.blit(title, (self.screen_w // 2 - title.get_width() // 2,
                              self.screen_h // 2 - 120))

        self._draw_btn(surface, self.btn_resume,   "Pokračovat")
        self._draw_btn(surface, self.btn_settings, "Nastavení")
        self._draw_btn(surface, self.btn_menu,     "Hlavní menu")

    def _draw_btn(self, surface, rect, label):
        hover  = rect.collidepoint(pygame.mouse.get_pos())
        bg     = get_c(self.skin, "pause_btn_hov") if hover else get_c(self.skin, "pause_btn_bg")
        border = get_c(self.skin, "pause_btn_brd")
        pygame.draw.rect(surface, bg, rect, border_radius=8)
        pygame.draw.rect(surface, border, rect, 2, border_radius=8)
        txt = self.font.render(label, True, get_c(self.skin, "btn_text"))
        surface.blit(txt, (rect.x + rect.w // 2 - txt.get_width() // 2,
                           rect.y + rect.h // 2 - txt.get_height() // 2))


# ---------------------------------------------------------------
class SettingsMenu:
    """Nastavení – hlasitost, FPS limit."""

    def __init__(self, screen_w, screen_h, font, settings: dict, skin="default"):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.skin = skin
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.settings = settings
        self.action = None

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
        bg = (220, 210, 245) if self.skin == "default" else (15, 10, 25)
        surface.fill(bg)

        title_c = get_c(self.skin, "title")
        title = self.title_font.render("Nastavení", True, title_c)
        surface.blit(title, (self.screen_w // 2 - title.get_width() // 2, 100))

        self._draw_setting(surface, "Hlasitost", self.settings["volume"],
                           self.vol_minus, self.vol_plus, 280, suffix="%")
        self._draw_setting(surface, "FPS limit", self.settings["fps"],
                           self.fps_minus, self.fps_plus, 360)

        hover = self.btn_back.collidepoint(pygame.mouse.get_pos())
        bg_c  = get_c(self.skin, "btn_hover") if hover else get_c(self.skin, "btn_bg")
        pygame.draw.rect(surface, bg_c, self.btn_back, border_radius=8)
        pygame.draw.rect(surface, get_c(self.skin, "btn_border"), self.btn_back, 2, border_radius=8)
        bt = self.font.render("Zpět", True, get_c(self.skin, "btn_text"))
        surface.blit(bt, (self.btn_back.x + self.btn_back.w // 2 - bt.get_width() // 2,
                          self.btn_back.y + 12))

    def _draw_setting(self, surface, label, value, btn_minus, btn_plus, y, suffix=""):
        cx    = self.screen_w // 2
        lbl_c = get_c(self.skin, "sub")
        lbl   = self.font.render(label, True, lbl_c)
        surface.blit(lbl, (cx - lbl.get_width() // 2, y - 30))

        for btn, sym in [(btn_minus, "−"), (btn_plus, "+")]:
            hover = btn.collidepoint(pygame.mouse.get_pos())
            bg_c  = get_c(self.skin, "btn_hover") if hover else get_c(self.skin, "btn_bg")
            pygame.draw.rect(surface, bg_c, btn, border_radius=6)
            pygame.draw.rect(surface, get_c(self.skin, "btn_border"), btn, 2, border_radius=6)
            s = self.font.render(sym, True, get_c(self.skin, "btn_text"))
            surface.blit(s, (btn.x + btn.w // 2 - s.get_width() // 2,
                             btn.y + btn.h // 2 - s.get_height() // 2))

        val_c   = get_c(self.skin, "title")
        val_txt = self.font.render(f"{value}{suffix}", True, val_c)
        surface.blit(val_txt, (cx - val_txt.get_width() // 2, y + 2))


# ---------------------------------------------------------------
class GameOverScreen:
    """Obrazovka konce hry (prohra nebo výhra)."""

    def __init__(self, screen_w, screen_h, font, won: bool,
                 has_next_level: bool = False, message: str = "", skin="default"):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.skin = skin
        self.title_font = pygame.font.SysFont("Arial", 52, bold=True)
        self.msg_font   = pygame.font.SysFont("Arial", 26)
        self.won = won
        self.has_next_level = has_next_level
        self.message = message
        self.action = None

        cx = screen_w // 2
        cy = screen_h // 2

        if won and has_next_level:
            self.btn_next    = pygame.Rect(cx - 110, cy - 80, 220, 55)
            self.btn_restart = pygame.Rect(cx - 110, cy - 10, 220, 55)
            self.btn_menu    = pygame.Rect(cx - 110, cy + 60,  220, 55)
        else:
            self.btn_next    = None
            self.btn_restart = pygame.Rect(cx - 110, cy - 10, 220, 55)
            self.btn_menu    = pygame.Rect(cx - 110, cy + 60,  220, 55)

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

        color = get_c(self.skin, "win_color") if self.won else get_c(self.skin, "lose_color")
        label = "Výhra!" if self.won else "Prohrál jsi!"
        title = self.title_font.render(label, True, color)
        surface.blit(title, (self.screen_w // 2 - title.get_width() // 2,
                              self.screen_h // 2 - 150))

        if self.message:
            msg_c   = get_c(self.skin, "win_color") if self.won else get_c(self.skin, "lose_color")
            msg_surf = self.msg_font.render(self.message, True, msg_c)
            surface.blit(msg_surf, (self.screen_w // 2 - msg_surf.get_width() // 2,
                                    self.screen_h // 2 - 90))

        if self.btn_next:
            self._draw_btn(surface, self.btn_next, "Další level",
                           bg=get_c(self.skin, "next_btn_bg"),
                           hov=get_c(self.skin, "next_btn_hov"),
                           brd=get_c(self.skin, "next_btn_brd"),
                           txt=get_c(self.skin, "next_btn_txt"))

        self._draw_btn(surface, self.btn_restart, "Znovu")
        self._draw_btn(surface, self.btn_menu,    "Menu")

    def _draw_btn(self, surface, rect, label,
                  bg=None, hov=None, brd=None, txt=None):
        bg  = bg  or get_c(self.skin, "over_btn_bg")
        hov = hov or get_c(self.skin, "over_btn_hov")
        brd = brd or get_c(self.skin, "over_btn_brd")
        txt = txt or get_c(self.skin, "over_btn_txt")
        hover = rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, hov if hover else bg, rect, border_radius=10)
        pygame.draw.rect(surface, brd, rect, 2, border_radius=10)
        t = self.font.render(label, True, txt)
        surface.blit(t, (rect.x + rect.w // 2 - t.get_width() // 2,
                         rect.y + rect.h // 2 - t.get_height() // 2))