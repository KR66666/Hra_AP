"""
main.py – vstupní bod hry Tower Defense.

Spuštění:
    python main.py

Kompilace do .exe (Windows):
    pyinstaller --onefile --windowed --icon=assets/icon.ico main.py
"""

import pygame
import sys
import os

# Zajistí správné importy bez ohledu na to, odkud se skript spouští
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.menu import Menu, SettingsMenu
from src.ui.skin_selector import SkinSelector
from src.game import Game
from src.level import ALL_LEVELS


# ------------------------------------------------------------------
# Konstanty
# ------------------------------------------------------------------
SCREEN_W = 896   # 14 sloupců × 64
SCREEN_H = 592   # 8 řádků × 64 + HUD 80
FPS_DEFAULT = 60


def get_icon_path():
    """Vrátí cestu k ikoně i po kompilaci PyInstalleru."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "assets", "icon.png")
    return os.path.join("assets", "icon.png")


def main():
    pygame.init()
    pygame.display.set_caption("Tower Defense")

    # Ikona (pokud existuje a je ve správném formátu)
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        try:
            pygame.display.set_icon(pygame.image.load(icon_path))
        except pygame.error:
            pass  # ikona není nutná, hra funguje i bez ní

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    font = pygame.font.SysFont("Arial", 22, bold=True)

    settings = {
        "volume": 70,
        "fps": FPS_DEFAULT,
    }

    state = "menu"          # aktuální obrazovka
    level_idx = 0
    chosen_skin = "default"

    menu = Menu(SCREEN_W, SCREEN_H, font)
    settings_menu = SettingsMenu(SCREEN_W, SCREEN_H, font, settings)
    skin_selector = SkinSelector(SCREEN_W, SCREEN_H, font)
    game = None
    clock = pygame.time.Clock()

    # ------------------------------------------------------------------
    # Hlavní smyčka stavového automatu
    # ------------------------------------------------------------------
    while True:
        clock.tick(settings["fps"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ---- MENU ----
            if state == "menu":
                menu.handle_event(event)
                if menu.action == "play":
                    state = "skin"
                    skin_selector = SkinSelector(SCREEN_W, SCREEN_H, font)
                elif menu.action == "settings":
                    state = "settings_from_menu"
                    settings_menu = SettingsMenu(SCREEN_W, SCREEN_H, font, settings)
                elif menu.action == "quit":
                    pygame.quit()
                    sys.exit()

            # ---- SKIN SELECTOR ----
            elif state == "skin":
                skin_selector.handle_event(event)
                if skin_selector.confirmed:
                    chosen_skin = skin_selector.chosen_skin
                    level_idx = 0
                    game = Game(screen, level_idx, settings, chosen_skin)
                    state = "game"

            # ---- NASTAVENÍ (z menu) ----
            elif state == "settings_from_menu":
                settings_menu.handle_event(event)
                if settings_menu.action == "back":
                    state = "menu"

            # ---- HRA ----
            # (game.run() blokuje – události řeší sama)

        # ------------------------------------------------------------------
        # Kreslení + přechody
        # ------------------------------------------------------------------
        if state == "menu":
            menu.draw(screen)

        elif state == "skin":
            skin_selector.draw(screen)

        elif state == "settings_from_menu":
            settings_menu.draw(screen)

        elif state == "game":
            if game is None:
                game = Game(screen, level_idx, settings, chosen_skin)

            # Spustíme herní smyčku (blokující)
            result = game.run()

            if result == "quit":
                pygame.quit()
                sys.exit()
            elif result == "menu":
                state = "menu"
                game = None
            elif result and result.startswith("level_"):
                # Restart stejného levelu
                level_idx = int(result.split("_")[1])
                game = Game(screen, level_idx, settings, chosen_skin)
            else:
                # Přechod na další level nebo menu
                if game.state == "gameover" and game.game_over_screen:
                    if game.game_over_screen.won and level_idx + 1 < len(ALL_LEVELS):
                        level_idx += 1
                        game = Game(screen, level_idx, settings, chosen_skin)
                    else:
                        state = "menu"
                        game = None
                else:
                    state = "menu"
                    game = None

        pygame.display.flip()


if __name__ == "__main__":
    main()