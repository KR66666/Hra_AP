from src.entities.enemy import BasicEnemy, FastEnemy, TankEnemy, FlyingEnemy, BossEnemy

CELL = 64


def build_path_pixels(path_cells, screen_w=None, screen_h=None):
    """Převede buňkové souřadnice na px souřadnice.První a poslední bod posunuty na okraj obrazovky."""
    pts = [(c * CELL + CELL // 2, r * CELL + CELL // 2) for c, r in path_cells]
    if len(pts) < 2:
        return pts

    x0, y0 = pts[0]
    x1, y1 = pts[1]
    if   x1 > x0: pts[0] = (0, y0)
    elif x1 < x0: pts[0] = (screen_w or x0 + CELL, y0)
    elif y1 > y0: pts[0] = (x0, 0)
    else:          pts[0] = (x0, screen_h or y0 + CELL)

    xn, yn = pts[-1]
    xp, yp = pts[-2]
    if   xn > xp: pts[-1] = (screen_w or xn + CELL, yn)
    elif xn < xp: pts[-1] = (0, yn)
    elif yn > yp: pts[-1] = (xn, screen_h or yn + CELL)
    else:          pts[-1] = (xn, 0)

    return pts

LEVEL1 = {
    "name": "Lesní stezka",
    "rows": 8,
    "cols": 14,
    "grid": [
        "##############",  
        "PPPP..........",  
        "###P..........",  
        "###PPPP.......",  
        "######P.......",  
        "######PPPPP...",  
        "...........P..",  
        "...........PPP",  
    ],
    "path_cells": [
        (0,1),(1,1),(2,1),(3,1),
        (3,2),
        (3,3),(4,3),(5,3),(6,3),
        (6,4),
        (6,5),(7,5),(8,5),(9,5),(10,5),
        (10,6),
        (10,7),(11,7),(12,7),(13,7),
    ],
    "waves": [
        [(BasicEnemy, 8, 1.2)],
        [(BasicEnemy, 6, 1.0), (FastEnemy, 4, 0.8)],
        [(TankEnemy, 2, 3.0), (FastEnemy, 6, 0.7)],
        [(FlyingEnemy, 5, 1.0), (BasicEnemy, 5, 1.0)],
        [(BossEnemy, 1, 0.0), (FastEnemy, 8, 0.6)],
    ],
    "start_gold": 180,
    "lives": 5,
    "bg_color": (34, 85, 34),
    "path_color": (160, 120, 60),
}

LEVEL2 = {
    "name": "Pouštní pevnost",
    "rows": 8,
    "cols": 14,
    "grid": [
        "##############",  
        "PPP...........",  
        "##P...........",  
        "##PPPP........",  
        "#####P........",  
        "#####PPPP.....",  
        "########P.....",  
        "########PPPPPP",  
    ],
    "path_cells": [
        (0,1),(1,1),(2,1),
        (2,2),
        (2,3),(3,3),(4,3),(5,3),
        (5,4),
        (5,5),(6,5),(7,5),(8,5),
        (8,6),
        (8,7),(9,7),(10,7),(11,7),(12,7),(13,7),
    ],
    "waves": [
        [(BasicEnemy, 10, 1.0)],
        [(FastEnemy, 8, 0.7), (BasicEnemy, 5, 1.0)],
        [(TankEnemy, 3, 2.5), (BasicEnemy, 8, 0.8)],
        [(FlyingEnemy, 6, 0.9), (FastEnemy, 6, 0.7)],
        [(TankEnemy, 2, 3.0), (FlyingEnemy, 4, 1.0), (FastEnemy, 6, 0.6)],
        [(BasicEnemy, 10, 0.5), (TankEnemy, 3, 2.0)],
        [(BossEnemy, 1, 0.0), (FastEnemy, 10, 0.5), (FlyingEnemy, 5, 0.8)],
    ],
    "start_gold": 220,
    "lives": 5,
    "bg_color": (160, 120, 50),
    "path_color": (200, 165, 90),
}

ALL_LEVELS = [LEVEL1, LEVEL2]