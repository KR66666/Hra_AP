"""
src/skins.py – Definice vizuálních skinů.

Každý skin definuje barvy pro:
  - pozadí mapy, cestu, mřížku
  - každý typ věže
  - každý typ nepřítele
  - UI panel
"""

SKINS = {
    # ------------------------------------------------------------------
    # KLASICKÝ – středověká fantasy, zelená příroda
    # ------------------------------------------------------------------
    "default": {
        "name": "Středověk",
        "desc": "Kamenné věže, zelené lesy.",
 
        "bg":          (28, 68, 28),
        "path":        (139, 105, 55),
        "path_edge":   (180, 145, 90),
        "grid_line":   (0, 0, 0),
        "wall":        (38, 38, 38),
 
        "panel_bg":    (25, 25, 20),
        "panel_line":  (70, 70, 50),
 
        "towers": {
            "ArrowTower":  {"body": (50, 140, 50),  "accent": (160, 210, 80),  "detail": (200, 160, 60)},
            "CannonTower": {"body": (70, 70, 160),  "accent": (100, 100, 220), "detail": (50, 50, 120)},
            "FreezeTower": {"body": (50, 170, 210), "accent": (180, 230, 255), "detail": (100, 200, 240)},
        },
 
        "enemies": {
            "BasicEnemy":  {"body": (210, 55, 55),   "inner": (255, 110, 110)},
            "FastEnemy":   {"body": (240, 190, 0),   "inner": (255, 220, 60)},
            "TankEnemy":   {"body": (70, 70, 190),   "inner": (40,  40, 130)},
            "FlyingEnemy": {"body": (140, 45, 210),  "inner": (190, 100, 255)},
            "BossEnemy":   {"body": (170, 15, 15),   "crown": (255, 210, 0)},
        },
    },
 
    # ------------------------------------------------------------------
    # TEMNÝ – post-apokalyptická krajina, oheň a rez
    # ------------------------------------------------------------------
    "dark": {
        "name": "Apokalypsa",
        "desc": "Spálená země, ohnivé věže.",
 
        "bg":          (18, 12, 8),
        "path":        (90, 55, 20),
        "path_edge":   (160, 80, 20),
        "grid_line":   (40, 20, 10),
        "wall":        (30, 15, 5),
 
        "panel_bg":    (15, 8, 5),
        "panel_line":  (100, 50, 10),
 
        "towers": {
            "ArrowTower":  {"body": (160, 60, 10),  "accent": (230, 100, 20), "detail": (255, 150, 50)},
            "CannonTower": {"body": (100, 20, 20),  "accent": (200, 40, 40),  "detail": (80, 10, 10)},
            "FreezeTower": {"body": (20, 80, 120),  "accent": (40, 160, 200), "detail": (80, 200, 240)},
        },
 
        "enemies": {
            "BasicEnemy":  {"body": (200, 80, 10),  "inner": (255, 130, 40)},
            "FastEnemy":   {"body": (220, 40, 40),  "inner": (255, 80, 80)},
            "TankEnemy":   {"body": (60, 40, 10),   "inner": (40, 25, 5)},
            "FlyingEnemy": {"body": (180, 100, 0),  "inner": (240, 160, 20)},
            "BossEnemy":   {"body": (120, 10, 10),  "crown": (220, 80, 0)},
        },
    },
 
    # ------------------------------------------------------------------
    # NEON – cyberpunk město, žáření a neon
    # ------------------------------------------------------------------
    "neon": {
        "name": "Cyberpunk",
        "desc": "Neonové světlo, digitální krajina.",
 
        "bg":          (5, 5, 18),
        "path":        (15, 15, 40),
        "path_edge":   (0, 200, 255),
        "grid_line":   (0, 40, 80),
        "wall":        (10, 10, 30),
 
        "panel_bg":    (5, 5, 20),
        "panel_line":  (0, 180, 255),
 
        "towers": {
            "ArrowTower":  {"body": (0, 180, 120),  "accent": (0, 255, 180),  "detail": (0, 220, 150)},
            "CannonTower": {"body": (180, 0, 180),  "accent": (255, 0, 255),  "detail": (120, 0, 120)},
            "FreezeTower": {"body": (0, 120, 220),  "accent": (0, 200, 255),  "detail": (80, 220, 255)},
        },
 
        "enemies": {
            "BasicEnemy":  {"body": (255, 30, 80),  "inner": (255, 100, 140)},
            "FastEnemy":   {"body": (255, 200, 0),  "inner": (255, 240, 80)},
            "TankEnemy":   {"body": (100, 0, 200),  "inner": (60,  0, 140)},
            "FlyingEnemy": {"body": (0, 220, 200),  "inner": (80, 255, 240)},
            "BossEnemy":   {"body": (200, 0, 100),  "crown": (255, 50, 200)},
        },
    },
}
 
 
def get_skin(skin_id: str) -> dict:
    return SKINS.get(skin_id, SKINS["default"])