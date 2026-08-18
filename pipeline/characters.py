"""Procedural 16x16 character sprites: 4 characters x 4 directions x 4-frame walk cycles."""
from __future__ import annotations

import random

from .pix import Canvas, shade, hash_seed

DIRS = ("down", "up", "left", "right")

SPECS = [
    {
        "id": "knight", "name": "Knight",
        "skin": (226, 184, 150), "hair": (90, 64, 48),
        "shirt": (154, 162, 176), "pants": (86, 74, 92), "shoes": (64, 56, 64),
        "accent": (196, 64, 64), "hat": "helm",
    },
    {
        "id": "villager", "name": "Villager",
        "skin": (216, 164, 128), "hair": (52, 46, 42),
        "shirt": (122, 150, 120), "pants": (94, 84, 64), "shoes": (72, 58, 44),
        "accent": (244, 214, 140), "hat": "none",
    },
    {
        "id": "wizard", "name": "Wizard",
        "skin": (236, 196, 158), "hair": (226, 226, 226),
        "shirt": (88, 76, 146), "pants": (88, 76, 146), "shoes": (54, 48, 74),
        "accent": (210, 182, 96), "hat": "cone", "robe": True,
    },
    {
        "id": "merchant", "name": "Merchant",
        "skin": (198, 142, 110), "hair": (62, 46, 32),
        "shirt": (188, 122, 92), "pants": (82, 66, 52), "shoes": (62, 48, 38),
        "accent": (72, 120, 160), "hat": "cap",
    },
]

_EYE = (22, 20, 26)


def _bob(phase):
    return 1 if phase in (1, 3) else 0


def _legs(c, pal, phase, xl, xr):
    dark = shade(pal["pants"], 0.8)
    if phase in (0, 2):
        for x in (xl, xl + 1):
            for y in (11, 12, 13):
                c.px(x, y, pal["pants"])
        for x in (xr, xr + 1):
            for y in (11, 12, 13):
                c.px(x, y, dark)
        for x in range(xl - 1, xl + 3):
            c.px(x, 14, pal["shoes"])
        for x in range(xr - 1, xr + 3):
            c.px(x, 14, pal["shoes"])
    elif phase == 1:
        for x in (xl, xl + 1):
            for y in (11, 12):
                c.px(x, y, pal["pants"])
        for x in range(xl - 1, xl + 3):
            c.px(x, 13, pal["shoes"])
        for x in (xr, xr + 1):
            for y in (11, 12, 13):
                c.px(x, y, dark)
        for x in range(xr - 1, xr + 3):
            c.px(x, 14, pal["shoes"])
    else:
        for x in (xr, xr + 1):
            for y in (11, 12):
                c.px(x, y, dark)
        for x in range(xr - 1, xr + 3):
            c.px(x, 13, shade(pal["shoes"], 0.85))
        for x in (xl, xl + 1):
            for y in (11, 12, 13):
                c.px(x, y, pal["pants"])
        for x in range(xl - 1, xl + 3):
            c.px(x, 14, pal["shoes"])


def _robe(c, pal):
    for y in range(11, 14):
        for x in range(5, 11):
            c.px(x, y, pal["pants"])
    for x in range(4, 12):
        c.px(x, 14, pal["accent"])


def _draw_front(c, pal, phase):
    bob = _bob(phase)
    R = lambda y: y + bob if y <= 10 else y  # noqa: E731
    for x in range(4, 12):
        c.px(x, R(0), pal["hair"]); c.px(x, R(1), pal["hair"])
    for x in range(3, 13):
        c.px(x, R(2), pal["hair"]); c.px(x, R(3), pal["hair"])
    for x in range(4, 12):
        c.px(x, R(4), pal["hair"]); c.px(x, R(5), pal["hair"])
    for y in range(2, 7):
        for x in range(5, 11):
            c.px(x, R(y), pal["skin"])
    for x in (6, 9):
        c.px(x, R(4), _EYE)
    c.px(7, R(6), shade(pal["skin"], 0.62)); c.px(8, R(6), shade(pal["skin"], 0.62))
    for x in range(6, 10):
        c.px(x, R(7), shade(pal["skin"], 0.88))
    for x in range(4, 12):
        c.px(x, R(8), pal["shirt"])
    for x in range(5, 11):
        c.px(x, R(9), pal["shirt"]); c.px(x, R(10), pal["shirt"])
    for x in (4, 11):
        c.px(x, R(9), pal["skin"]); c.px(x, R(10), pal["skin"])
    for x in range(5, 11):
        c.px(x, R(10), pal["accent"])
    if pal.get("robe"):
        _robe(c, pal)
        return
    _legs(c, pal, phase, 5, 9)


def _draw_back(c, pal, phase):
    bob = _bob(phase)
    R = lambda y: y + bob if y <= 10 else y  # noqa: E731
    for y in range(0, 7):
        for x in range(3, 13):
            c.px(x, R(y), pal["hair"])
    c.px(5, R(2), shade(pal["hair"], 1.3))
    for x in range(6, 10):
        c.px(x, R(7), shade(pal["skin"], 0.88))
    for x in range(4, 12):
        c.px(x, R(8), pal["shirt"])
    for x in range(5, 11):
        c.px(x, R(9), pal["shirt"]); c.px(x, R(10), pal["shirt"])
    for x in range(5, 11):
        c.px(x, R(10), pal["accent"])
    if pal.get("robe"):
        _robe(c, pal)
        return
    _legs(c, pal, phase, 5, 9)


def _draw_side(c, pal, phase):
    bob = _bob(phase)
    R = lambda y: y + bob if y <= 10 else y  # noqa: E731
    for x in range(5, 10):
        c.px(x, R(0), pal["hair"]); c.px(x, R(1), pal["hair"])
    for y in range(2, 7):
        for x in range(6, 10):
            c.px(x, R(y), pal["hair"])
    for y in range(2, 7):
        for x in range(3, 9):
            c.px(x, R(y), pal["skin"])
    c.px(4, R(4), _EYE)
    c.px(4, R(5), shade(pal["skin"], 0.85))
    for x in range(5, 8):
        c.px(x, R(7), shade(pal["skin"], 0.88))
    for x in range(4, 11):
        c.px(x, R(8), pal["shirt"])
    for x in range(5, 11):
        c.px(x, R(9), pal["shirt"]); c.px(x, R(10), pal["shirt"])
    for x in (4,):
        c.px(x, R(9), pal["skin"]); c.px(x, R(10), pal["skin"])
    for x in range(5, 11):
        c.px(x, R(10), pal["accent"])
    if pal.get("robe"):
        _robe(c, pal)
        return
    _legs(c, pal, phase, 5, 9)


def _hat(c, pal, d, phase):
    bob = _bob(phase)
    R = lambda y: y + bob  # noqa: E731
    kind = pal.get("hat")
    if not kind:
        return
    if kind == "helm":
        a, l, dk, v = pal["shirt"], shade(pal["shirt"], 1.25), shade(pal["shirt"], 0.75), (28, 28, 34)
        if d == "left":
            x0, x1 = 4, 10
        else:
            x0, x1 = 4, 12
        for x in range(x0, x1):
            c.px(x, R(0), l); c.px(x, R(1), l)
            c.px(x, R(2), a); c.px(x, R(3), a)
            c.px(x, R(5), a); c.px(x, R(6), a)
        c.px(x0, R(4), dk); c.px(x1 - 1, R(4), dk)
        for x in range(x0 + 1, x1 - 1):
            c.px(x, R(4), v)
    elif kind == "cone":
        a, t = pal["accent"], pal["shirt"]
        if d == "left":
            x0, x1, b0, b1 = 5, 10, 3, 11
        else:
            x0, x1, b0, b1 = 6, 10, 4, 12
        c.px(x0, R(0), t); c.px(x1 - 1, R(0), t)
        c.px(x0, R(1), t); c.px(x0 + 1, R(1), t); c.px(x1 - 1, R(1), t)
        c.px(x0 + 1, R(1), a)
        for x in range(b0, b1):
            c.px(x, R(2), a)
        for x in range(b0, b1):
            c.px(x, R(3), shade(a, 0.8))
    elif kind == "cap":
        a = pal["accent"]
        if d == "left":
            x0, x1, b0, b1 = 5, 10, 3, 11
        else:
            x0, x1, b0, b1 = 5, 11, 4, 12
        for x in range(x0, x1):
            c.px(x, R(0), a); c.px(x, R(1), a); c.px(x, R(2), shade(a, 0.85))
        for x in range(b0, b1):
            c.px(x, R(3), shade(a, 0.8))


def make_character(spec, seed):
    """Return dict direction -> list of 4 frame Canvases (idle, stride, idle, stride)."""
    out = {}
    for d in DIRS:
        frames = []
        for phase in range(4):
            c = Canvas(16, 16)
            if d == "down":
                _draw_front(c, spec, phase)
            elif d == "up":
                _draw_back(c, spec, phase)
            elif d == "left":
                _draw_side(c, spec, phase)
            else:
                _draw_side(c, spec, phase)
                c.flip_x()
            _hat(c, spec, d, phase)
            frames.append(c)
        out[d] = frames
    return out


def make_all_characters(seed):
    return [(spec, make_character(spec, hash_seed(seed, spec["id"]))) for spec in SPECS]
