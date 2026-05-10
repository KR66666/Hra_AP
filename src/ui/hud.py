import pygame

class HUD:
    PANEL_H = 80
    TOWER_BTNS = [
    {"name": "Lučištník", "cost": 80,  "key": "1", "color": (76, 120, 80)}, 
    {"name": "Dělo",      "cost": 150, "key": "2", "color": (90, 95, 140)}, 
    {"name": "Mrazič",    "cost": 120, "key": "3", "color": (70, 150, 170)}, 
]

    def __init__(self, screen_w, screen_h, font):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font
        self.small_font = pygame.font.SysFont("Arial", 14)
        self.tiny_font  = pygame.font.SysFont("Arial", 12)
        self.coin_img = pygame.image.load("assets/coin.png")
        self.coin_img = pygame.transform.scale(self.coin_img, (100, 100))
        self.game_area_h = screen_h - self.PANEL_H

        btn_w, btn_h = 100, 55
        start_x = 10
        self.btn_rects = []
        for i, btn in enumerate(self.TOWER_BTNS):
            rect = pygame.Rect(start_x + i * (btn_w + 6), screen_h - btn_h - 12, btn_w, btn_h)
            self.btn_rects.append(rect)

    
        delete_x = start_x + len(self.TOWER_BTNS) * (btn_w + 6) + 8
        delete_y  = screen_h - 45 - 22
        self.delete_btn = pygame.Rect(delete_x, delete_y, 55, 45)

        self.delete_mode = False

        self.wave_btn  = pygame.Rect(screen_w - 160, screen_h - 60, 150, 50)
        self.pause_btn = pygame.Rect(screen_w - 290, screen_h - 40, 100, 35)

    def draw(self, surface, lives, gold, wave_num, total_waves, wave_active, selected_tower_idx, gold_msg=""):
        panel_rect = pygame.Rect(0, self.screen_h - self.PANEL_H, self.screen_w, self.PANEL_H)
        pygame.draw.rect(surface, (30, 30, 30), panel_rect)
        pygame.draw.line(surface, (80, 80, 80),
                         (0, self.screen_h - self.PANEL_H),
                         (self.screen_w, self.screen_h - self.PANEL_H), 2)

        info_x = self.screen_w // 2 - 100
        surface.blit(self.font.render(f"❤  {lives}", True, (220, 80, 80)),
                     (info_x, self.screen_h - self.PANEL_H + 8))
        surface.blit(self.coin_img, (info_x + 110, self.screen_h - self.PANEL_H - 4))
        surface.blit(self.font.render(f"{gold}", True, (226, 252, 53)),
                     (info_x + 180, self.screen_h - self.PANEL_H + 30))
        surface.blit(self.font.render(f"Vlna {wave_num}/{total_waves}", True, (200, 200, 200)),
                     (info_x + 260, self.screen_h - self.PANEL_H + 8))

        if gold_msg:
            surface.blit(self.small_font.render(gold_msg, True, (255, 100, 100)),
                         (info_x, self.screen_h - self.PANEL_H + 56))

        for i, (btn_data, rect) in enumerate(zip(self.TOWER_BTNS, self.btn_rects)):
            selected = (i == selected_tower_idx) and not self.delete_mode
            border = (255, 220, 0) if selected else (80, 80, 80)
            pygame.draw.rect(surface, btn_data["color"], rect, border_radius=6)
            pygame.draw.rect(surface, border, rect, 2, border_radius=6)
            surface.blit(self.small_font.render(f"[{btn_data['key']}] {btn_data['name']}", True, (255,255,255)),
                         (rect.x + 5, rect.y + 7))
            surface.blit(self.small_font.render(f"{btn_data['cost']}", True, (220,190,50)),
                         (rect.x + 5, rect.y + 28))

        del_color  = (140, 30, 30) if self.delete_mode else (80, 30, 30)
        del_border = (255, 90, 90) if self.delete_mode else (140, 60, 60)
        pygame.draw.rect(surface, del_color,  self.delete_btn, border_radius=6)
        pygame.draw.rect(surface, del_border, self.delete_btn, 2, border_radius=6)
        if self.delete_mode:
            pygame.draw.rect(surface, (255, 50, 50), self.delete_btn, 3, border_radius=6)

        icon = self.small_font.render("[X]", True, (255, 200, 200))
        surface.blit(icon, (self.delete_btn.x + self.delete_btn.w // 2 - icon.get_width() // 2,
                            self.delete_btn.y + 6))

        txt = self.tiny_font.render("Smazat", True, (255, 180, 180))
        surface.blit(txt, (self.delete_btn.x + self.delete_btn.w // 2 - txt.get_width() // 2,
                           self.delete_btn.y + 26))

        #PAUZA, TLAČITKO
        pygame.draw.rect(surface, (60, 60, 100), self.pause_btn, border_radius=6)
        pygame.draw.rect(surface, (120, 120, 160), self.pause_btn, 2, border_radius=6)
        surface.blit(self.font.render("Pauza", True, (200,200,220)),
                     (self.pause_btn.x + 5, self.pause_btn.y + 7))

        #TLAČITKO VLNA
        wave_color = (26, 196, 48) if not wave_active else (80, 80, 80)
        pygame.draw.rect(surface, wave_color, self.wave_btn, border_radius=6)
        pygame.draw.rect(surface, (100, 200, 100), self.wave_btn, 2, border_radius=6)
        label = "Spustit vlnu" if not wave_active else "Vlna probíhá..."
        surface.blit(self.small_font.render(label, True, (220,255,220)),
                     (self.wave_btn.x + 6, self.wave_btn.y + 16))

    def get_clicked_tower(self, pos):
        for i, rect in enumerate(self.btn_rects):
            if rect.collidepoint(pos): return i
        return None

    def clicked_delete_btn(self, pos): return self.delete_btn.collidepoint(pos)
    def clicked_wave_btn(self, pos):   return self.wave_btn.collidepoint(pos)
    def clicked_pause_btn(self, pos):  return self.pause_btn.collidepoint(pos)
    