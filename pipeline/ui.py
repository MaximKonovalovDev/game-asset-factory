"""Procedural 16x16 UI kit: buttons, 9-slice panel pieces, frame, icons."""
from __future__ import annotations

import random

from .pix import Canvas, shade, hash_seed

BG = (56, 48, 80)
BG_LIGHT = (74, 64, 104)
BG_DARK = (40, 34, 60)
BORDER = (26, 22, 40)
GOLD = (216, 178, 110)
GOLD_DARK = (150, 116, 70)


def _button(hover=False, pressed=False):
    c = Canvas(16, 16)
    fill = BG_DARK if pressed else (BG_LIGHT if hover else BG)
    for y in range(16):
        for x in range(16):
            inside = True
            if y == 0 or y == 15:
                inside = 3 <= x <= 12
            elif y == 1 or y == 14:
                inside = 2 <= x <= 13
            else:
                inside = 1 <= x <= 14
            if not inside:
                continue
            if y in (0, 1, 14, 15) or x in (0, 1, 14, 15):
                c.px(x, y, GOLD if hover else BORDER)
            else:
                c.px(x, y, fill)
    if pressed:
        for x in range(3, 13):
            c.px(x, 3, shade(fill, 0.8)); c.px(x, 4, shade(fill, 0.85))
        for x in range(3, 13):
            c.px(x, 12, shade(fill, 1.2)); c.px(x, 13, shade(fill, 1.1))
    else:
        for x in range(3, 13):
            c.px(x, 3, shade(fill, 1.25)); c.px(x, 4, shade(fill, 1.12))
        for x in range(3, 13):
            c.px(x, 12, shade(fill, 0.82)); c.px(x, 13, shade(fill, 0.9))
    return c


def _frame():
    c = Canvas(16, 16)
    for x in range(16):
        c.px(x, 0, GOLD); c.px(x, 1, GOLD_DARK)
        c.px(x, 14, GOLD_DARK); c.px(x, 15, BORDER)
    for y in range(16):
        c.px(0, y, GOLD); c.px(1, y, GOLD_DARK)
        c.px(14, y, GOLD_DARK); c.px(15, y, BORDER)
    return c


def _panel_bg(seed, name):
    c = Canvas(16, 16)
    rng = random.Random(hash_seed(seed, name))
    for y in range(16):
        for x in range(16):
            v = rng.random()
            c.px(x, y, BG if v < 0.85 else shade(BG, 0.88))
    return c


def _panel_slices(seed):
    """Return the nine 9-slice pieces. Border width is 2 px."""
    bg = _panel_bg(seed, "panel")
    pieces = {}

    def with_border(name, top, bottom, left, right):
        c = bg.__class__(16, 16)
        for y in range(16):
            for x in range(16):
                c.px(x, y, bg.get(x, y))
        for y in range(16):
            for x in range(16):
                edge = (y < top or y >= 16 - bottom or x < left or x >= 16 - right)
                if edge:
                    c.px(x, y, GOLD if (y < 1 or x < 1) and (y >= 16 - 2 or x >= 16 - 2) else GOLD_DARK)
        return c

    pieces["panel_corner_tl"] = with_border("tl", 2, 0, 2, 0)
    pieces["panel_corner_tr"] = with_border("tr", 2, 0, 0, 2)
    pieces["panel_corner_bl"] = with_border("bl", 0, 2, 2, 0)
    pieces["panel_corner_br"] = with_border("br", 0, 2, 0, 2)
    pieces["panel_edge_top"] = with_border("top", 2, 0, 0, 0)
    pieces["panel_edge_bottom"] = with_border("bottom", 0, 2, 0, 0)
    pieces["panel_edge_left"] = with_border("left", 0, 0, 2, 0)
    pieces["panel_edge_right"] = with_border("right", 0, 0, 0, 2)
    pieces["panel_center"] = bg
    return pieces


def _stamp(c, pattern, colors, ox=0, oy=0):
    for y, row in enumerate(pattern):
        for x, ch in enumerate(row):
            if ch != "." and ch in colors:
                c.px(x + ox, y + oy, colors[ch])


def make_icons():
    icons = {}
    Y, D, W = GOLD, GOLD_DARK, (255, 250, 220)

    c = Canvas(16, 16)
    _stamp(c, [
        ".LL......LL.",
        ".LLL....LLL.",
        "LLLLL..LLLL.",
        "LLLLLLLLLLLL",
        ".LLLLLLLLLL.",
        "..LLLLLLLL..",
        "...LLLLLL...",
        "....LLLL....",
        ".....LL.....",
    ], {"L": (216, 70, 80)}, 2, 3)
    icons["icon_heart"] = c

    c = Canvas(16, 16)
    _stamp(c, [
        "...YYYY...",
        "..YYYYYY..",
        ".YYYWWYYY.",
        "YYYWWWYYYY",
        "YYYWYYYYYY",
        "YYYYYYYYYY",
        ".YYYYYYYY.",
        "..YYYYYY..",
        "...YYYY...",
        "....YY....",
    ], {"Y": Y, "W": W}, 3, 3)
    icons["icon_coin"] = c

    c = Canvas(16, 16)
    steel, steel_l = (168, 176, 190), (208, 216, 228)
    for i in range(8):
        c.px(11 - i, 2 + i, steel)
    for i in range(1, 6):
        c.px(10 - i, 2 + i, steel_l)
    c.px(12, 3, steel_l)
    for x in (9, 10, 11):
        c.px(x, 10, Y); c.px(x, 11, Y)
    c.px(11, 12, D); c.px(12, 12, Y); c.px(12, 13, D)
    icons["icon_sword"] = c

    c = Canvas(16, 16)
    _stamp(c, [
        "..XXXXXXXX..",
        ".XXXXXXXXXX.",
        ".XXXXXXXXXX.",
        ".XGGGGGGGGX.",
        ".XGGGGGGGGX.",
        ".XGGGGGGGGX.",
        ".XGGGGGGGGX.",
        ".XXXXXXXXXX.",
        "..XXXXXXXX..",
        "..XXXXXXXX..",
        "...XXXXXX...",
        "....XXXX....",
    ], {"X": (168, 176, 190), "G": (120, 128, 145)}, 1, 1)
    c.px(8, 2, W)
    icons["icon_shield"] = c

    c = Canvas(16, 16)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if 2 <= dx * dx + dy * dy <= 4:
                c.px(3 + dx, 4 + dy, Y)
    for y in range(6, 13):
        c.px(6, y, Y)
        c.px(5, y, D)
    c.px(7, 11, Y); c.px(7, 12, Y); c.px(8, 11, Y)
    icons["icon_key"] = c

    c = Canvas(16, 16)
    _stamp(c, [
        "...CC...",
        "...CC...",
        "..GGGG..",
        ".GLLLLG.",
        ".GLLLLG.",
        ".GLLLLG.",
        ".GLLLLG.",
        ".GLLLLG.",
        ".GLLLLG.",
        ".GGGGGG.",
        "..GGGG..",
        "...GG...",
    ], {"G": (168, 216, 240), "L": (232, 90, 80), "C": (140, 100, 60)}, 3, 1)
    c.px(5, 5, W)
    icons["icon_potion"] = c

    c = Canvas(16, 16)
    _stamp(c, [
        "....YY....",
        "...YYYY...",
        "..YYYYYY..",
        ".YYYYYYYY.",
        "YYYYYYYYYY",
        "YYYYYYYYYY",
        ".YYYYYYYY.",
        "..YYYYYY..",
        "...YYYY...",
        "....YY....",
    ], {"Y": Y}, 3, 3)
    c.px(6, 4, W); c.px(5, 8, D)
    icons["icon_star"] = c

    c = Canvas(16, 16)
    _stamp(c, [
        "XXXXXXXXXX",
        "XWWWWWWWWX",
        "XXXXXXXXXX",
        "XBBBBBBBBX",
        "XBBBBBBBBX",
        "XBBBBBBBBX",
        "XBBBBBBBBX",
        "XXXXXXXXXX",
    ], {"X": (104, 70, 46), "W": (170, 124, 86), "B": (142, 98, 64)}, 2, 3)
    c.px(5, 5, Y); c.px(6, 5, Y)
    c.px(4, 6, Y); c.px(7, 6, Y)
    icons["icon_chest"] = c

    c = Canvas(16, 16)
    _stamp(c, [
        "....GG....",
        "...GGLG...",
        "..GGLGGG..",
        ".GGLGGGGG.",
        "GGGLGGGGGG",
        "GGGGGGGGGG",
        ".GGRRGGGG.",
        "..GGRRRG..",
        "...GRRR...",
        "....RR....",
    ], {"G": (120, 220, 200), "L": (240, 255, 250), "R": (60, 140, 130)}, 2, 3)
    icons["icon_gem"] = c

    c = Canvas(16, 16)
    for y in range(2, 14):
        for x in (1, 2, 3, 12, 13, 14):
            c.px(x, y, (120, 96, 64))
    for y in range(2, 14):
        for x in range(4, 12):
            c.px(x, y, (214, 190, 140))
    for y in range(2, 14):
        c.px(7, y, (170, 148, 104)); c.px(8, y, (170, 148, 104))
    c.px(9, 5, (216, 80, 80)); c.px(10, 6, (216, 80, 80))
    c.px(10, 5, (216, 80, 80)); c.px(9, 6, (216, 80, 80))
    icons["icon_map"] = c

    c = Canvas(16, 16)
    for x in (4, 8, 12):
        c.px(x, 1, Y)
    for x in range(3, 14):
        c.px(x, 2, Y)
    for x in range(2, 14):
        c.px(x, 3, Y); c.px(x, 4, Y)
    for x in range(2, 14):
        c.px(x, 5, D)
    c.px(5, 4, (232, 90, 90)); c.px(8, 4, (90, 160, 232)); c.px(11, 4, (110, 200, 120))
    icons["icon_crown"] = c

    return icons


def make_ui_kit(seed):
    """Return an ordered dict of all UI kit elements (name -> Canvas)."""
    items = {}
    items["button_normal"] = _button()
    items["button_hover"] = _button(hover=True)
    items["button_pressed"] = _button(pressed=True)
    items["frame"] = _frame()
    for k, v in _panel_slices(seed).items():
        items[k] = v
    for k, v in make_icons().items():
        items[k] = v
    return items


NINE_SLICE = {
    "border": 2,
    "corners": ["panel_corner_tl", "panel_corner_tr", "panel_corner_bl", "panel_corner_br"],
    "edges_h": ["panel_edge_top", "panel_edge_bottom"],
    "edges_v": ["panel_edge_left", "panel_edge_right"],
    "center": ["panel_center"],
}
