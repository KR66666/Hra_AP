"""
Definice levelů – cesty, vlny nepřátel, mapa políček.
'path' = seznam (col, row) políček kudy jdou nepřátelé.
'waves' = seznam vln, každá vlna je seznam (typ, počet, interval_s).
'grid' = seznam řetězců; 'P'=cesta, '.'=volné pole, '#'=zeď.
"""

from src.entities.enemy import BasicEnemy, FastEnemy, TankEnemy, FlyingEnemy, BossEnemy

CELL = 64  # velikost jednoho políčka v pixelech


def build_path_pixels(path_cells):
    """Převede buňkové souřadnice na středové px souřadnice."""
    return [(c * CELL + CELL // 2, r * CELL + CELL // 2) for c, r in path_cells]


# ------------------------------------------------------------------
# LEVEL 1 – Jednoduchá mapa
# ------------------------------------------------------------------
LEVEL1 = {
    "name": "Lesní stezka",
    "rows": 8,
    "cols": 14,
    # P = cesta,  . = staveniště,  # = dekorace/zeď
    "grid": [
        "##############",
        "#PPPP.......##",
        "####P.......##",
        "####PPPP....##",
        "#######P....##",
        "#######PPPPP.#",
        "..........P..#",
        "..........P..#",
    ],
    "path_cells": [
        (1,1),(2,1),(3,1),(4,1),
        (4,2),
        (4,3),(5,3),(6,3),(7,3),
        (7,4),
        (7,5),(8,5),(9,5),(10,5),(11,5),
        (11,6),(11,7),
    ],
    "waves": [
        # vlna 1 – jen základní
        [(BasicEnemy, 8, 1.2)],
        # vlna 2 – základní + rychlí
        [(BasicEnemy, 6, 1.0), (FastEnemy, 4, 0.8)],
        # vlna 3 – tank + rychlí
        [(TankEnemy, 2, 3.0), (FastEnemy, 6, 0.7)],
        # vlna 4 – létající + základní
        [(FlyingEnemy, 5, 1.0), (BasicEnemy, 5, 1.0)],
        # vlna 5 – BOSS
        [(BossEnemy, 1, 0.0), (FastEnemy, 8, 0.6)],
    ],
    "start_gold": 180,
    "lives": 20,
    "bg_color": (34, 85, 34),
    "path_color": (160, 120, 60),
}


# ------------------------------------------------------------------
# LEVEL 2 – Složitější mapa se zatáčkami
# ------------------------------------------------------------------
LEVEL2 = {
    "name": "Pouštní pevnost",
    "rows": 10,
    "cols": 16,
    "grid": [
        "################",
        "#PPP............",
        "##P..............",
        "##PPPP..........",
        "#####P..........",
        "#####PPPP.......",
        "########P.......",
        "########PPPP....",
        "###########P....",
        "###########PPP..",
    ],
    "path_cells": [
        (1,1),(2,1),(3,1),
        (3,2),
        (3,3),(4,3),(5,3),(6,3),
        (6,4),
        (6,5),(7,5),(8,5),(9,5),
        (9,6),
        (9,7),(10,7),(11,7),(12,7),
        (12,8),
        (12,9),(13,9),(14,9),
    ],
    "waves": [
        # vlna 1
        [(BasicEnemy, 10, 1.0)],
        # vlna 2
        [(FastEnemy, 8, 0.7), (BasicEnemy, 5, 1.0)],
        # vlna 3
        [(TankEnemy, 3, 2.5), (BasicEnemy, 8, 0.8)],
        # vlna 4
        [(FlyingEnemy, 6, 0.9), (FastEnemy, 6, 0.7)],
        # vlna 5
        [(TankEnemy, 2, 3.0), (FlyingEnemy, 4, 1.0), (FastEnemy, 6, 0.6)],
        # vlna 6
        [(BasicEnemy, 10, 0.5), (TankEnemy, 3, 2.0)],
        # vlna 7 – BOSS + přisluhovači
        [(BossEnemy, 1, 0.0), (FastEnemy, 10, 0.5), (FlyingEnemy, 5, 0.8)],
    ],
    "start_gold": 220,
    "lives": 15,
    "bg_color": (180, 140, 60),
    "path_color": (200, 170, 100),
}

ALL_LEVELS = [LEVEL1, LEVEL2]