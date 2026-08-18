"""Procedural 16x16 tile generators for the four built-in themes.

Every tile is drawn from scratch with a seeded RNG — no copied art, no AI.
Each theme returns (tiles, meta) where tiles maps name -> Canvas and
meta["collision"] maps tile name -> 0 (walkable) / 1 (solid).
"""
from __future__ import annotations

import random

from .palette import GRASS, CAVE, SEASIDE, DESERT
from .pix import Canvas, blob, shade, speckle, hash_seed

SIZE = 16


def _rng(seed, name):
    return random.Random(hash_seed(seed, name))


def _tex(c, rng, p, base, light, dark, density=0.32):
    speckle(c, rng, base, light, dark, density=density)


# ---------------------------------------------------------------- grass ----

def _grass_base(seed):
    rng = _rng(seed, "grass")
    c = Canvas(SIZE, SIZE)
    _tex(c, rng, GRASS, GRASS["grass"], GRASS["grass_light"], GRASS["grass_dark"])
    return c


def _blades(c, rng, n=5):
    for _ in range(n):
        x, y = rng.randrange(1, 15), rng.randrange(2, 13)
        col = GRASS["grass_light"] if rng.random() < 0.6 else GRASS["grass"]
        c.px(x, y, col)
        if rng.random() < 0.6:
            c.px(x, y + 1, shade(col, 0.85))


def _tuft(c, rng, x, y):
    for dx in range(-1, 2):
        c.px(x + dx, y, GRASS["grass_light"])
        c.px(x + dx, y - 1, GRASS["grass"])
    c.px(x, y - 2, GRASS["grass_light"])


def _flower(c, rng, cx, cy, color):
    c.px(cx - 1, cy - 1, color)
    c.px(cx + 1, cy - 1, color)
    c.px(cx - 1, cy + 1, color)
    c.px(cx + 1, cy + 1, color)
    c.px(cx, cy, GRASS["white"])


def grass_tiles(seed):
    tiles = {}
    coll = {}

    c = _grass_base(seed)
    rng = _rng(seed, "grass_blades")
    _blades(c, rng)
    tiles["grass"] = c
    coll["grass"] = 0

    c = _grass_base(seed)
    rng = _rng(seed, "tuft")
    for _ in range(3):
        _tuft(c, rng, rng.randrange(2, 14), rng.randrange(3, 13))
    tiles["grass_tuft"] = c
    coll["grass_tuft"] = 0

    c = _grass_base(seed)
    rng = _rng(seed, "flower")
    _flower(c, rng, rng.randrange(3, 13), rng.randrange(3, 12),
            GRASS["flower_yellow"] if rng.random() < 0.6 else GRASS["flower_red"])
    tiles["grass_flower"] = c
    coll["grass_flower"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "dirt")
    _tex(c, rng, GRASS, GRASS["dirt"], GRASS["dirt_light"], GRASS["dirt_dark"])
    tiles["dirt"] = c
    coll["dirt"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "dirt_pebbles")
    _tex(c, rng, GRASS, GRASS["dirt"], GRASS["dirt_light"], GRASS["dirt_dark"])
    for _ in range(4):
        x, y = rng.randrange(2, 14), rng.randrange(2, 14)
        c.px(x, y, GRASS["rock_light"])
        if rng.random() < 0.6:
            c.px(x + 1, y, shade(GRASS["rock_light"], 0.85))
    tiles["dirt_pebbles"] = c
    coll["dirt_pebbles"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "path")
    for x in range(SIZE):
        for y in (0, 1, 13, 14, 15):
            c.px(x, y, GRASS["grass"] if rng.random() < 0.8 else GRASS["grass_dark"])
    for y in range(2, 13):
        for x in range(SIZE):
            v = rng.random()
            if v < 0.1:
                c.px(x, y, GRASS["dirt_light"])
            elif v < 0.22:
                c.px(x, y, GRASS["dirt_dark"])
            else:
                c.px(x, y, GRASS["dirt"])
    for y in (2, 12):
        for x in range(SIZE):
            if rng.random() < 0.5:
                c.px(x, y, GRASS["grass"])
    tiles["path"] = c
    coll["path"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "tree")
    for y in range(8, 15):
        for x in range(6, 9):
            c.px(x, y, GRASS["wood"])
    for y in range(8, 15):
        c.px(5, y, GRASS["wood_dark"])
        c.px(9, y, GRASS["wood_dark"])
    c.px(5, 14, GRASS["wood_dark"]); c.px(9, 14, GRASS["wood_dark"])
    c.px(6, 15, GRASS["wood_dark"]); c.px(8, 15, GRASS["wood_dark"])
    blob(c, rng, 5, 4, 3, GRASS["leaf_dark"])
    blob(c, rng, 10, 4, 3, GRASS["leaf_dark"])
    blob(c, rng, 7, 2, 4, GRASS["leaf"])
    for _ in range(6):
        c.px(rng.randrange(3, 12), rng.randrange(0, 5), GRASS["grass_light"])
    tiles["tree"] = c
    coll["tree"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "rock")
    blob(c, rng, 8, 9, 4, GRASS["rock"])
    blob(c, rng, 6, 7, 1, GRASS["rock_light"])
    blob(c, rng, 10, 11, 2, GRASS["rock_dark"])
    c.px(5, 8, GRASS["leaf"]); c.px(6, 10, GRASS["leaf"])
    tiles["rock"] = c
    coll["rock"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "bush")
    blob(c, rng, 5, 10, 3, GRASS["leaf_dark"])
    blob(c, rng, 10, 10, 3, GRASS["leaf_dark"])
    blob(c, rng, 8, 8, 3, GRASS["leaf"])
    for _ in range(4):
        c.px(rng.randrange(4, 12), rng.randrange(6, 9), GRASS["grass_light"])
    tiles["bush"] = c
    coll["bush"] = 1

    for f in range(4):
        c = Canvas(SIZE, SIZE)
        rng = _rng(seed, f"water_frame_{f}")
        for y in range(SIZE):
            for x in range(SIZE):
                c.px(x, y, GRASS["water"])
        for y in range(SIZE):
            for x in range(SIZE):
                band = (y + f) % 3
                if band == 0 and (x + f) % 4 < 2:
                    c.px(x, y, GRASS["water_light"])
                elif band == 1 and (x + f) % 4 >= 2:
                    c.px(x, y, GRASS["water_deep"])
        for _ in range(4):
            c.px(rng.randrange(1, 15), rng.randrange(1, 15), GRASS["white"])
        tiles[f"water_{f}"] = c
        coll[f"water_{f}"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "bridge")
    for y in range(SIZE):
        for x in range(SIZE):
            c.px(x, y, GRASS["water"])
    for y in (3, 4, 12, 13):
        for x in (0, 1, 14, 15):
            c.px(x, y, GRASS["wood_dark"])
    for y in range(5, 12):
        for x in range(2, 14):
            c.px(x, y, GRASS["wood"])
        for x in range(2, 14):
            if x % 4 == 3:
                c.px(x, y, GRASS["wood_dark"])
        if y == 5:
            for x in range(2, 14):
                c.px(x, y, GRASS["wood_light"])
    for x in range(2, 14):
        c.px(x, 11, GRASS["wood_dark"])
    tiles["bridge"] = c
    coll["bridge"] = 0

    return tiles, {"collision": coll}


# ----------------------------------------------------------------- cave ----

def cave_tiles(seed):
    tiles = {}
    coll = {}

    def floor(name, extra=None):
        c = Canvas(SIZE, SIZE)
        rng = _rng(seed, name)
        _tex(c, rng, CAVE, CAVE["stone"], CAVE["stone_light"], CAVE["stone_dark"])
        if extra:
            extra(c, rng)
        return c

    def pit(c, rng):
        for _ in range(5):
            x, y = rng.randrange(1, 14), rng.randrange(1, 14)
            c.px(x, y, CAVE["stone_deep"])
            c.px(x + 1, y, CAVE["stone_deep"])

    def pebbles(c, rng):
        for _ in range(4):
            x, y = rng.randrange(1, 14), rng.randrange(1, 14)
            c.px(x, y, CAVE["stone_light"])
            if rng.random() < 0.5:
                c.px(x + 1, y, CAVE["stone_light"])

    def moss(c, rng):
        for _ in range(4):
            blob(c, rng, rng.randrange(3, 13), rng.randrange(3, 13), 2, CAVE["moss"])
        for _ in range(4):
            c.px(rng.randrange(1, 15), rng.randrange(1, 15), CAVE["moss_light"])

    def gems(c, rng):
        for _ in range(3):
            x, y = rng.randrange(2, 13), rng.randrange(2, 13)
            g = rng.choice([CAVE["gem_teal"], CAVE["gem_pink"], CAVE["gem_violet"]])
            c.px(x, y, g); c.px(x + 1, y, g)
            c.px(x, y + 1, shade(g, 0.8)); c.px(x + 1, y + 1, shade(g, 0.8))
            c.px(x, y, CAVE["white"] if False else shade(g, 1.35))

    tiles["stone_floor"] = floor("stone_floor", pit)
    coll["stone_floor"] = 0
    tiles["stone_pebbles"] = floor("stone_pebbles", pebbles)
    coll["stone_pebbles"] = 0
    tiles["moss_floor"] = floor("moss_floor", moss)
    coll["moss_floor"] = 0
    tiles["gems_floor"] = floor("gems_floor", gems)
    coll["gems_floor"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "stone_wall")
    _tex(c, rng, CAVE, CAVE["stone"], CAVE["stone_light"], CAVE["stone_dark"])
    for y in range(0, 3):
        for x in range(SIZE):
            c.px(x, y, CAVE["stone_deep"])
    for x in range(SIZE):
        if rng.random() < 0.6:
            c.px(x, 3, CAVE["stone_deep"])
    for _ in range(4):
        x = rng.randrange(0, 16)
        for y in range(4, rng.randrange(7, 10)):
            c.px(x, y, CAVE["stone_deep"])
    tiles["stone_wall"] = c
    coll["stone_wall"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "crystal")
    _tex(c, rng, CAVE, CAVE["stone"], CAVE["stone_light"], CAVE["stone_dark"])
    for y in range(4, 13):
        c.px(6, y, CAVE["gem_teal"]); c.px(9, y, CAVE["gem_teal"])
    for y in range(5, 12):
        c.px(7, y, shade(CAVE["gem_teal"], 1.25)); c.px(8, y, shade(CAVE["gem_teal"], 0.75))
    c.px(6, 4, shade(CAVE["gem_teal"], 0.7)); c.px(9, 4, shade(CAVE["gem_teal"], 0.7))
    for x in range(6, 10):
        c.px(x, 13, shade(CAVE["gem_teal"], 0.6))
    tiles["crystal"] = c
    coll["crystal"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "stalagmite")
    _tex(c, rng, CAVE, CAVE["stone"], CAVE["stone_light"], CAVE["stone_dark"])
    for (bx, h) in ((2, 6), (7, 8), (12, 5)):
        for y in range(SIZE - 1 - h, SIZE):
            c.px(bx, y, CAVE["stone"])
            c.px(bx + 1, y, CAVE["stone_dark"])
        c.px(bx, SIZE - 1 - h, shade(CAVE["stone_light"], 0.9))
    tiles["stalagmite"] = c
    coll["stalagmite"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "water_pool")
    for y in range(0, 6):
        for x in range(SIZE):
            v = rng.random()
            c.px(x, y, CAVE["stone"] if v < 0.7 else (CAVE["stone_light"] if v < 0.85 else CAVE["stone_dark"]))
    for y in range(6, SIZE):
        for x in range(SIZE):
            c.px(x, y, CAVE["water"])
    for y in range(7, SIZE):
        for x in range(SIZE):
            if (y + x) % 5 == 0:
                c.px(x, y, CAVE["water_light"])
    for _ in range(3):
        c.px(rng.randrange(1, 15), rng.randrange(8, 15), shade(CAVE["water_light"], 1.2))
    for y in range(13, SIZE):
        for x in range(SIZE):
            if rng.random() < 0.7:
                c.px(x, y, CAVE["water_deep"])
    tiles["water_pool"] = c
    coll["water_pool"] = 1

    return tiles, {"collision": coll}


# --------------------------------------------------------------- seaside ----

def seaside_tiles(seed):
    tiles = {}
    coll = {}
    P = SEASIDE

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "sand")
    _tex(c, rng, P, P["sand"], P["sand_light"], P["sand_dark"])
    tiles["sand"] = c
    coll["sand"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "sand_ripple")
    _tex(c, rng, P, P["sand"], P["sand_light"], P["sand_dark"])
    for y in range(SIZE):
        for x in range(SIZE):
            if (x + y) % 6 < 2:
                c.px(x, y, P["sand_light"])
    tiles["sand_ripple"] = c
    coll["sand_ripple"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "shell")
    _tex(c, rng, P, P["sand"], P["sand_light"], P["sand_dark"])
    c.px(5, 9, P["shell"]); c.px(6, 9, P["shell"]); c.px(6, 8, P["shell"])
    c.px(5, 8, shade(P["shell"], 0.8))
    tiles["shell"] = c
    coll["shell"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "shallow")
    for y in range(5):
        for x in range(SIZE):
            c.px(x, y, P["sand"])
    for y in range(5, 8):
        for x in range(SIZE):
            c.px(x, y, shade(P["sand"], 0.85) if rng.random() < 0.5 else P["shallow"])
    for y in range(8, SIZE):
        for x in range(SIZE):
            c.px(x, y, P["shallow"])
    for _ in range(3):
        c.px(rng.randrange(1, 15), rng.randrange(9, 15), P["water_light"])
    tiles["shallow"] = c
    coll["shallow"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "deep")
    for y in range(SIZE):
        for x in range(SIZE):
            t = y / SIZE
            c.px(x, y, shade(P["water"], 1.0 - 0.45 * t))
    for y in range(SIZE):
        for x in range(SIZE):
            if (y + x) % 6 == 0:
                c.px(x, y, P["water_light"])
    for _ in range(3):
        c.px(rng.randrange(1, 15), rng.randrange(1, 15), P["foam"])
    tiles["deep"] = c
    coll["deep"] = 1

    for f in range(4):
        c = Canvas(SIZE, SIZE)
        rng = _rng(seed, f"wave_{f}")
        for y in range(SIZE):
            for x in range(SIZE):
                t = y / SIZE
                c.px(x, y, shade(P["water"], 1.0 - 0.45 * t))
        for y in range(SIZE):
            for x in range(SIZE):
                band = (y + f) % 4
                if band == 0 and (x + f) % 3 < 2:
                    c.px(x, y, P["foam"])
                elif band == 1 and (x + f) % 4 >= 2:
                    c.px(x, y, P["water_light"])
        for _ in range(3):
            c.px(rng.randrange(1, 15), rng.randrange(1, 15), P["foam"])
        tiles[f"wave_{f}"] = c
        coll[f"wave_{f}"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "rock")
    blob(c, rng, 8, 9, 4, P["rock"])
    blob(c, rng, 6, 7, 1, P["rock_light"])
    blob(c, rng, 10, 11, 2, P["rock_dark"])
    tiles["rock"] = c
    coll["rock"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "pier")
    for y in range(SIZE):
        for x in range(SIZE):
            c.px(x, y, P["water"])
    for y in range(3, 13):
        for x in (0, 1, 14, 15):
            c.px(x, y, P["wood_dark"])
    for y in range(6, 11):
        for x in range(2, 14):
            c.px(x, y, P["wood"])
        for x in range(2, 14):
            if x % 4 == 3:
                c.px(x, y, P["wood_dark"])
        if y == 6:
            for x in range(2, 14):
                c.px(x, y, P["wood_light"])
    for x in range(2, 14):
        c.px(x, 10, P["wood_dark"])
    tiles["pier"] = c
    coll["pier"] = 0

    return tiles, {"collision": coll}


# ---------------------------------------------------------------- desert ----

def desert_tiles(seed):
    tiles = {}
    coll = {}
    P = DESERT

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "sand")
    _tex(c, rng, P, P["sand"], P["sand_light"], P["sand_dark"])
    tiles["sand"] = c
    coll["sand"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "sand_ripple")
    _tex(c, rng, P, P["sand"], P["sand_light"], P["sand_dark"])
    for y in range(SIZE):
        for x in range(SIZE):
            if (x + y) % 6 < 2:
                c.px(x, y, P["sand_light"])
    tiles["sand_ripple"] = c
    coll["sand_ripple"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "dune")
    _tex(c, rng, P, P["sand"], P["sand_light"], P["sand_dark"])
    for y in range(6, 9):
        for x in range(SIZE):
            c.px(x, y, P["sand_light"])
    for y in range(9, 12):
        for x in range(SIZE):
            if rng.random() < 0.6:
                c.px(x, y, shade(P["sand"], 0.88))
    tiles["dune"] = c
    coll["dune"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "cactus")
    for y in range(8, 14):
        for x in range(6, 10):
            c.px(x, y, P["cactus"])
    for x in (5, 9):
        for y in range(7, 15):
            c.px(x, y, P["cactus_dark"])
    for y in range(9, 12):
        c.px(4, y, P["cactus"]); c.px(5, y, P["cactus"])
    c.px(4, 12, P["cactus_dark"])
    for y in range(9, 12):
        c.px(11, y, P["cactus"]); c.px(10, y, P["cactus"])
    c.px(11, 12, P["cactus_dark"])
    for x in range(6, 9):
        c.px(x, 13, P["cactus_light"])
    c.px(5, 7, P["flower_yellow"] if False else P["cactus_light"])
    c.px(9, 7, P["cactus_light"])
    tiles["cactus"] = c
    coll["cactus"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "dry_bush")
    blob(c, rng, 8, 9, 3, P["bush"])
    for _ in range(5):
        c.px(rng.randrange(3, 13), rng.randrange(6, 12), P["bush_dark"])
    tiles["dry_bush"] = c
    coll["dry_bush"] = 0

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "rock")
    blob(c, rng, 8, 9, 4, P["rock"])
    blob(c, rng, 6, 7, 1, P["rock_light"])
    blob(c, rng, 10, 11, 2, P["rock_dark"])
    tiles["rock"] = c
    coll["rock"] = 1

    c = Canvas(SIZE, SIZE)
    rng = _rng(seed, "oasis")
    for y in range(4):
        for x in range(SIZE):
            c.px(x, y, P["sand"])
    for y in range(4, SIZE):
        for x in range(SIZE):
            c.px(x, y, P["water"])
    for y in range(5, SIZE):
        for x in range(SIZE):
            if (y + x) % 5 == 0:
                c.px(x, y, P["water_light"])
    for _ in range(4):
        c.px(rng.randrange(1, 15), rng.randrange(6, 15), shade(P["water_light"], 1.2))
    tiles["oasis"] = c
    coll["oasis"] = 1

    return tiles, {"collision": coll}


BUILDERS = {
    "grass": grass_tiles,
    "cave": cave_tiles,
    "water": seaside_tiles,
    "desert": desert_tiles,
}


def make_tiles(theme, seed):
    """Return (tiles: dict[name->Canvas], meta: dict)."""
    return BUILDERS[theme](seed)
