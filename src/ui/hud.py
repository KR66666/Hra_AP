import pygame

class HUD:
    """
    Herní HUD – zobrazuje životy, zlato, vlnu a panel věží.
    """

    PANEL_H = 80
    TOWER_BTNS = [
        {"name": "Lučištník", "cost": 80,  "key": "1", "color": (60, 160, 60)},
        {"name": "Dělo",      "cost": 150, "key": "2", "color": (80, 80, 160)},
        {"name": "Mrazič",    "cost": 120, "key": "3", "color": (60, 180, 220)},
    ]

    def __init__(self, screen_w, screen_h, font):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.small_font = pygame.font.SysFont("Arial", 15)

        self.coin_img = pygame.image.load("assets/coin.png")
        self.coin_img = pygame.transform.scale(self.coin_img, (100, 100))

        # Výška herní plochy = screen_h - panel
        self.game_area_h = screen_h - self.PANEL_H

        # Tlačítka věží
        btn_w = 130
        btn_h = 60
        start_x = 10
        self.btn_rects = []
        for i, btn in enumerate(self.TOWER_BTNS):
            rect = pygame.Rect(start_x + i * (btn_w + 8), screen_h - btn_h - 10, btn_w, btn_h)
            self.btn_rects.append(rect)

        # Tlačítko SMAZAT – hned za tlačítky věží
        delete_x = start_x + len(self.TOWER_BTNS) * (btn_w + 8) + 10
        self.delete_btn = pygame.Rect(delete_x, screen_h - btn_h - 10, 100, btn_h)

        # Režim mazání
        self.delete_mode = False

        # Tlačítko "Spustit vlnu"
        self.wave_btn = pygame.Rect(screen_w - 160, screen_h - 60, 150, 50)

        # Tlačítko Pauza
        self.pause_btn = pygame.Rect(screen_w - 290, screen_h - 40, 100, 35)

    def draw(self, surface, lives, gold, wave_num, total_waves, wave_active, selected_tower_idx, gold_msg=""):
        # Panel pozadí
        panel_rect = pygame.Rect(0, self.screen_h - self.PANEL_H, self.screen_w, self.PANEL_H)
        pygame.draw.rect(surface, (30, 30, 30), panel_rect)
        pygame.draw.line(surface, (80, 80, 80), (0, self.screen_h - self.PANEL_H),
                         (self.screen_w, self.screen_h - self.PANEL_H), 2)

        # Info: životy, zlato, vlna
        info_x = self.screen_w // 2 - 100
        life_txt = self.font.render(f"❤  {lives}", True, (220, 80, 80))
        gold_txt = self.font.render(f"{gold}", True, (226, 252, 53))
        wave_txt = self.font.render(f"Vlna {wave_num}/{total_waves}", True, (200, 200, 200))
        surface.blit(life_txt, (info_x, self.screen_h - self.PANEL_H + 8))
        surface.blit(self.coin_img, (info_x + 110, self.screen_h - self.PANEL_H - 4))
        surface.blit(gold_txt, (info_x + 180, self.screen_h - self.PANEL_H + 30))
        surface.blit(wave_txt, (info_x + 260, self.screen_h - self.PANEL_H + 8))

        # Zpráva (málo zlata apod.)
        if gold_msg:
            msg = self.small_font.render(gold_msg, True, (255, 100, 100))
            surface.blit(msg, (info_x, self.screen_h - self.PANEL_H + 36))

        # Tlačítka věží
        for i, (btn_data, rect) in enumerate(zip(self.TOWER_BTNS, self.btn_rects)):
            color = btn_data["color"]
            selected = (i == selected_tower_idx) and not self.delete_mode
            border = (255, 220, 0) if selected else (80, 80, 80)
            pygame.draw.rect(surface, color, rect, border_radius=6)
            pygame.draw.rect(surface, border, rect, 2, border_radius=6)
            name_s = self.small_font.render(f"[{btn_data['key']}] {btn_data['name']}", True, (255, 255, 255))
            cost_s = self.small_font.render(f"⬡ {btn_data['cost']}", True, (220, 190, 50))
            surface.blit(name_s, (rect.x + 6, rect.y + 8))
            surface.blit(cost_s, (rect.x + 6, rect.y + 30))

        # Tlačítko SMAZAT
        del_color = (160, 40, 40) if self.delete_mode else (80, 30, 30)
        del_border = (255, 80, 80) if self.delete_mode else (140, 60, 60)
        pygame.draw.rect(surface, del_color, self.delete_btn, border_radius=6)
        pygame.draw.rect(surface, del_border, self.delete_btn, 2, border_radius=6)
        del_label = self.small_font.render("[Smazat", True, (255, 200, 200))
        del_sub   = self.small_font.render("věž", True, (255, 180, 180))
        surface.blit(del_label, (self.delete_btn.x + 8, self.delete_btn.y + 8))
        surface.blit(del_sub,   (self.delete_btn.x + 28, self.delete_btn.y + 30))
        if self.delete_mode:
            pygame.draw.rect(surface, (255, 50, 50), self.delete_btn, 3, border_radius=6)

        # Tlačítko Pauza
        pygame.draw.rect(surface, (60, 60, 100), self.pause_btn, border_radius=6)
        pygame.draw.rect(surface, (120, 120, 160), self.pause_btn, 2, border_radius=6)
        p_txt = self.font.render("Pauza", True, (200, 200, 220))
        surface.blit(p_txt, (self.pause_btn.x + 5, self.pause_btn.y + 7))

        # Tlačítko Vlna
        wave_color = (26, 196, 48) if not wave_active else (80, 80, 80)
        pygame.draw.rect(surface, wave_color, self.wave_btn, border_radius=6)
        pygame.draw.rect(surface, (100, 200, 100), self.wave_btn, 2, border_radius=6)
        label = "Spustit vlnu" if not wave_active else "Vlna probíhá..."
        w_txt = self.small_font.render(label, True, (220, 255, 220))
        surface.blit(w_txt, (self.wave_btn.x + 6, self.wave_btn.y + 16))

    def get_clicked_tower(self, pos):
        for i, rect in enumerate(self.btn_rects):
            if rect.collidepoint(pos):
                return i
        return None

    def clicked_delete_btn(self, pos):
        return self.delete_btn.collidepoint(pos)

    def clicked_wave_btn(self, pos):
        return self.wave_btn.collidepoint(pos)

    def clicked_pause_btn(self, pos):
        return self.pause_btn.collidepoint(pos)