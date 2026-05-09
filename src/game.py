import pygame
import math

from src.level import ALL_LEVELS, build_path_pixels, CELL
from src.entities.tower import ArrowTower, CannonTower, FreezeTower
from src.entities.enemy import BasicEnemy, FastEnemy, TankEnemy, FlyingEnemy, BossEnemy
from src.ui.hud import HUD
from src.menu import PauseMenu, GameOverScreen


TOWER_CLASSES = [ArrowTower, CannonTower, FreezeTower]
TOWER_COSTS   = [80, 150, 120]


class Game:
    """
    Hlavní herní třída – řídí herní smyčku, entity, vlny a UI.
    """

    def __init__(self, screen: pygame.Surface, level_idx: int, settings: dict, skin: str):
        self.screen = screen
        self.screen_w, self.screen_h = screen.get_size()
        self.settings = settings
        self.skin = skin
        self.level_data = ALL_LEVELS[level_idx]
        self.level_idx = level_idx

        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.clock = pygame.time.Clock()

        self._load_level()

        self.hud = HUD(self.screen_w, self.screen_h, self.font)
        self.pause_menu = PauseMenu(self.screen_w, self.screen_h, self.font, skin=self.skin)
        self.game_over_screen = None

        self.state = "playing"
        self.selected_tower_idx = 0
        self.hover_cell = None
        self.gold_msg = ""
        self.gold_msg_timer = 0.0

    # ------------------------------------------------------------------
    def _load_level(self):
        ld = self.level_data
        self.lives = ld["lives"]
        self.gold  = ld["start_gold"]
        # Tmavý skin přepíše barvy mapy
        if self.skin == "dark":
            self.bg_color   = (12, 10, 20)
            self.path_color = (140, 60, 20)
        else:
            self.bg_color   = (240, 248, 230)
            self.path_color = ld["path_color"]
        self.grid  = ld["grid"]
        self.rows  = ld["rows"]
        self.cols  = ld["cols"]
        self.path_px = build_path_pixels(ld["path_cells"], self.screen_w, self.screen_h - 80)
        self.path_cells_set = set(map(tuple, ld["path_cells"]))

        self.towers:      list = []
        self.enemies:     list = []
        self.projectiles: list = []

        self.waves = ld["waves"]
        self.current_wave = 0
        self.wave_active  = False
        self.spawn_queue  = []
        self.spawn_timer  = 0.0

    # ------------------------------------------------------------------
    # Hlavní smyčka
    # ------------------------------------------------------------------
    def run(self):
        while True:
            dt = self.clock.tick(self.settings["fps"]) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                result = self._handle_event(event)
                if result:
                    return result

            if self.state == "playing":
                self._update(dt)

            self._draw()
            pygame.display.flip()

    # ------------------------------------------------------------------
    # Události
    # ------------------------------------------------------------------
    def _handle_event(self, event):
        if self.state == "gameover":
            self.game_over_screen.handle_event(event)
            if self.game_over_screen.action == "menu":
                return "menu"
            if self.game_over_screen.action == "restart":
                return f"level_{self.level_idx}"
            if self.game_over_screen.action == "next":
                return f"level_{self.level_idx + 1}"
            return None

        if self.state == "paused":
            self.pause_menu.handle_event(event)
            if self.pause_menu.action == "resume":
                self.state = "playing"
            elif self.pause_menu.action == "menu":
                return "menu"
            return None

        # --- Klávesnice ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "paused"
            elif event.key == pygame.K_1:
                self.selected_tower_idx = 0
                self.hud.delete_mode = False
            elif event.key == pygame.K_2:
                self.selected_tower_idx = 1
                self.hud.delete_mode = False
            elif event.key == pygame.K_3:
                self.selected_tower_idx = 2
                self.hud.delete_mode = False
            elif event.key == pygame.K_x:
                self.hud.delete_mode = not self.hud.delete_mode

        # --- Myš ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            # Tlačítko smazat
            if self.hud.clicked_delete_btn(pos):
                self.hud.delete_mode = not self.hud.delete_mode
                return None

            # Tlačítka věží – přepne věž A vypne delete mode
            clicked = self.hud.get_clicked_tower(pos)
            if clicked is not None:
                self.selected_tower_idx = clicked
                self.hud.delete_mode = False
                return None

            if self.hud.clicked_pause_btn(pos):
                self.state = "paused"
                return None

            if self.hud.clicked_wave_btn(pos) and not self.wave_active:
                self._start_next_wave()
                return None

            # Klik do herní plochy
            if pos[1] < self.screen_h - HUD.PANEL_H:
                col = pos[0] // CELL
                row = pos[1] // CELL
                if self.hud.delete_mode:
                    self._try_delete_tower(col, row)
                else:
                    self._try_place_tower(col, row)

        if event.type == pygame.MOUSEMOTION:
            if event.pos[1] < self.screen_h - HUD.PANEL_H:
                self.hover_cell = (event.pos[0] // CELL, event.pos[1] // CELL)
            else:
                self.hover_cell = None

        return None

    # ------------------------------------------------------------------
    # Stavba věže
    # ------------------------------------------------------------------
    def _try_place_tower(self, col, row):
        if col >= self.cols or row >= self.rows:
            return
        if (col, row) in self.path_cells_set:
            self._show_msg("Nelze stavět na cestě!")
            return
        if row < len(self.grid) and col < len(self.grid[row]) and self.grid[row][col] == '#':
            self._show_msg("Nelze stavět zde!")
            return
        for t in self.towers:
            if int(t.x // CELL) == col and int(t.y // CELL) == row:
                self._show_msg("Pole je obsazené!")
                return

        cost = TOWER_COSTS[self.selected_tower_idx]
        if self.gold < cost:
            self._show_msg("Málo zlata!")
            return

        cls = TOWER_CLASSES[self.selected_tower_idx]
        self.towers.append(cls(col * CELL, row * CELL, CELL))
        self.gold -= cost

    # ------------------------------------------------------------------
    # Smazání věže – vrátí 60 % ceny zpět
    # ------------------------------------------------------------------
    def _try_delete_tower(self, col, row):
        for i, t in enumerate(self.towers):
            if int(t.x // CELL) == col and int(t.y // CELL) == row:
                # Vrátit 60 % ceny
                refund = int(t.cost * 0.6)
                self.gold += refund
                self.towers.pop(i)
                self._show_msg(f"Věž smazána (+{refund} zlata)")
                return
        self._show_msg("Zde žádná věž není.")

    def _show_msg(self, msg):
        self.gold_msg = msg
        self.gold_msg_timer = 2.0

    # ------------------------------------------------------------------
    # Vlny
    # ------------------------------------------------------------------
    def _start_next_wave(self):
        if self.current_wave >= len(self.waves):
            return
        self.wave_active = True
        wave = self.waves[self.current_wave]
        self.current_wave += 1

        abs_queue = []
        for enemy_cls, count, interval in wave:
            for i in range(count):
                abs_queue.append((enemy_cls, i * interval))
        abs_queue.sort(key=lambda x: x[1])

        self.spawn_queue = []
        prev = 0.0
        for cls, t in abs_queue:
            self.spawn_queue.append((cls, t - prev))
            prev = t
        self.spawn_timer = 0.0

    def _update_spawning(self, dt):
        if not self.spawn_queue:
            return
        self.spawn_timer += dt
        while self.spawn_queue and self.spawn_timer >= self.spawn_queue[0][1]:
            cls, delay = self.spawn_queue.pop(0)
            self.spawn_timer -= delay
            sx, sy = self.path_px[0]
            self.enemies.append(cls(sx - 16, sy - 16, self.path_px, self.skin))

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def _update(self, dt):
        if self.gold_msg_timer > 0:
            self.gold_msg_timer -= dt
            if self.gold_msg_timer <= 0:
                self.gold_msg = ""

        self._update_spawning(dt)

        # Nepřátelé – pokud dojdou do konce = ztráta života
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            enemy.update(dt)
            if enemy.reached_end and enemy.alive:
                self.lives -= 1
                enemy.destroy()
                self._show_msg(f"Nepřítel prošel! Životy: {self.lives}")

        # Prohra když životy = 0
        if self.lives <= 0:
            self.state = "gameover"
            self.game_over_screen = GameOverScreen(
                self.screen_w, self.screen_h, self.font, won=False,
                message="Prohrál jsi! Nepřítel prošel do konce.",
                skin=self.skin
            )
            return

        # Odměny za zabití
        for enemy in self.enemies:
            if not enemy.alive and enemy.reward > 0:
                self.gold += enemy.reward
                enemy.reward = 0

        self.enemies = [e for e in self.enemies if e.alive]

        # Věže
        for tower in self.towers:
            tower.update(dt, self.enemies, self.projectiles)

        # Střely
        for proj in self.projectiles:
            if proj.alive:
                proj.update(dt)
        self.projectiles = [p for p in self.projectiles if p.alive]

        # Vlna dokončena?
        if self.wave_active and not self.spawn_queue and not self.enemies:
            self.wave_active = False
            self.gold += 25

        # Výhra
        if (self.current_wave >= len(self.waves)
                and not self.wave_active
                and not self.enemies
                and self.lives > 0):
            self.state = "gameover"
            from src.level import ALL_LEVELS
            has_next = self.level_idx + 1 < len(ALL_LEVELS)
            self.game_over_screen = GameOverScreen(
                self.screen_w, self.screen_h, self.font, won=True,
                has_next_level=has_next,
                message="Level dokončen! Výborně!",
                skin=self.skin
            )

    # ------------------------------------------------------------------
    # Kreslení
    # ------------------------------------------------------------------
    def _draw(self):
        self.screen.fill(self.bg_color)
        self._draw_grid()
        self._draw_path()
        self._draw_hover()

        for t in self.towers:
            t.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        for p in self.projectiles:
            p.draw(self.screen)

        self.hud.draw(
            self.screen,
            self.lives, self.gold,
            self.current_wave, len(self.waves),
            self.wave_active,
            self.selected_tower_idx,
            self.gold_msg,
        )

        if self.state == "paused":
            self.pause_menu.draw(self.screen)
        if self.state == "gameover" and self.game_over_screen:
            self.game_over_screen.draw(self.screen)

    def _draw_grid(self):
        game_h = self.screen_h - HUD.PANEL_H
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * CELL, row * CELL, CELL, CELL)
                if rect.y + CELL > game_h:
                    continue
                ch = self.grid[row][col] if row < len(self.grid) and col < len(self.grid[row]) else '.'
                if ch == '#':
                    pygame.draw.rect(self.screen, (40, 40, 40), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def _draw_path(self):
        if len(self.path_px) < 2:
            return
        pygame.draw.lines(self.screen, self.path_color, False, self.path_px, CELL - 6)
        edge = tuple(min(255, c + 40) for c in self.path_color)
        pygame.draw.lines(self.screen, edge, False, self.path_px, 2)

    def _draw_hover(self):
        if not self.hover_cell:
            return
        col, row = self.hover_cell
        if col >= self.cols or row >= self.rows:
            return
        rect = pygame.Rect(col * CELL, row * CELL, CELL, CELL)
        surf = pygame.Surface((CELL, CELL), pygame.SRCALPHA)

        if self.hud.delete_mode:
            # Červená – mazací mód
            surf.fill((255, 60, 60, 80))
            self.screen.blit(surf, rect.topleft)
            # Zkříženě X přes pole
            pygame.draw.line(self.screen, (255, 60, 60),
                             rect.topleft, rect.bottomright, 2)
            pygame.draw.line(self.screen, (255, 60, 60),
                             rect.topright, rect.bottomleft, 2)
        else:
            can_place = (col, row) not in self.path_cells_set
            color = (100, 255, 100, 60) if can_place else (255, 80, 80, 60)
            surf.fill(color)
            self.screen.blit(surf, rect.topleft)
            if can_place:
                cls = TOWER_CLASSES[self.selected_tower_idx]
                dummy = cls(col * CELL, row * CELL, CELL)
                dummy.draw_range(self.screen)