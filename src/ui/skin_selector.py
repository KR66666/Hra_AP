import pygame


class SkinSelector:
    """
    Obrazovka pro výběr herního skinu před začátkem hry.
    """

    SKINS = [
        {
            "id": "default",
            "name": "Klasický",
            "desc": "Zelená příroda, kamenné věže.",
            "preview_colors": [(60, 160, 60), (80, 80, 160), (60, 180, 220)],
            "bg": (34, 85, 34),
        },
        {
            "id": "dark",
            "name": "Temný",
            "desc": "Temná krajina, ohnivé efekty.",
            "preview_colors": [(180, 40, 40), (80, 20, 120), (200, 80, 0)],
            "bg": (10, 10, 20),
        },
    ]

    def __init__(self, screen_w, screen_h, font):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.selected = 0
        self.confirmed = False
        self.chosen_skin = "default"

        card_w, card_h = 220, 260
        total_w = len(self.SKINS) * card_w + (len(self.SKINS) - 1) * 40
        start_x = (screen_w - total_w) // 2
        start_y = (screen_h - card_h) // 2 - 20

        self.card_rects = []
        for i in range(len(self.SKINS)):
            rect = pygame.Rect(start_x + i * (card_w + 40), start_y, card_w, card_h)
            self.card_rects.append(rect)

        self.confirm_btn = pygame.Rect(screen_w // 2 - 100, start_y + card_h + 30, 200, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.card_rects):
                if rect.collidepoint(event.pos):
                    self.selected = i
            if self.confirm_btn.collidepoint(event.pos):
                self.chosen_skin = self.SKINS[self.selected]["id"]
                self.confirmed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected = max(0, self.selected - 1)
            if event.key == pygame.K_RIGHT:
                self.selected = min(len(self.SKINS) - 1, self.selected + 1)
            if event.key == pygame.K_RETURN:
                self.chosen_skin = self.SKINS[self.selected]["id"]
                self.confirmed = True

    def draw(self, surface):
        surface.fill((230, 210, 245))

        title = self.title_font.render("Vyber si režim:", True, (60, 0, 120))
        surface.blit(title, (self.screen_w // 2 - title.get_width() // 2, 50))

        for i, (skin, rect) in enumerate(zip(self.SKINS, self.card_rects)):
            border_color = (255, 220, 0) if i == self.selected else (80, 80, 100)
            bg_color = (160, 120, 90) if i == self.selected else (130, 95, 70)
            pygame.draw.rect(surface, bg_color, rect, border_radius=12)
            pygame.draw.rect(surface, border_color, rect, 3, border_radius=12)

            for j, color in enumerate(skin["preview_colors"]):
                cr = pygame.Rect(rect.x + 20 + j * 62, rect.y + 20, 50, 50)
                pygame.draw.rect(surface, color, cr, border_radius=8)

            name_t = self.font.render(skin["name"], True, (255, 255, 255))
            desc_t = self.small_font.render(skin["desc"], True, (255, 255, 255))
            surface.blit(name_t, (rect.x + rect.w // 2 - name_t.get_width() // 2, rect.y + 90))
            surface.blit(desc_t, (rect.x + 10, rect.y + 130))

            if i == self.selected:
                sel = self.small_font.render("Vybráno", True, (0, 0, 0))
                surface.blit(sel, (rect.x + rect.w // 2 - sel.get_width() // 2, rect.y + 200))

        hover = self.confirm_btn.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, (140, 80, 180) if hover else (110, 60, 150), self.confirm_btn, border_radius=8)
        pygame.draw.rect(surface, (200, 150, 255), self.confirm_btn, 2, border_radius=8)
        btn_t = self.font.render("Potvrdit", True, (255, 255, 255))
        surface.blit(btn_t, (self.confirm_btn.x + self.confirm_btn.w // 2 - btn_t.get_width() // 2,
                             self.confirm_btn.y + 12))

        hint = self.small_font.render("← → pro výběr, Enter pro potvrzení", True, (120, 120, 140))
        surface.blit(hint, (self.screen_w // 2 - hint.get_width() // 2, self.screen_h - 40))