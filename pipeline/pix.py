"""Tiny pixel-drawing helpers. All drawing is deterministic (seeded rng)."""
from __future__ import annotations

import random
import zlib

from PIL import Image


def shade(c, f):
    """Multiply each channel by f, clamped to 0..255."""
    return tuple(max(0, min(255, round(v * f))) for v in c)


def hash_seed(base_seed, name):
    """Derive a per-artifact seed from a base seed and a stable name."""
    return (base_seed + zlib.crc32(name.encode("utf-8"))) & 0x7FFFFFFF


class Canvas:
    """A small RGBA pixel grid (default transparent background)."""

    def __init__(self, w, h, bg=None):
        self.w = w
        self.h = h
        self.bg = bg
        self.grid = [[bg for _ in range(w)] for _ in range(h)]

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.grid[y][x] = c

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.grid[y][x]
        return None

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def flip_x(self):
        self.grid = [row[::-1] for row in self.grid]

    def to_image(self):
        img = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        for y in range(self.h):
            for x in range(self.w):
                c = self.grid[y][x]
                if c is not None:
                    img.putpixel((x, y), (c[0], c[1], c[2], 255))
        return img


def blob(c, rng, cx, cy, r, col):
    """Fill a fuzzy circle with slight per-pixel brightness variation."""
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                v = rng.random()
                if v < 0.16:
                    c.px(x, y, shade(col, 1.18))
                elif v < 0.34:
                    c.px(x, y, shade(col, 0.86))
                else:
                    c.px(x, y, col)


def speckle(c, rng, base, light, dark, density=0.32, pit=0.05):
    """Fill the canvas with base color and scatter light/dark pixels."""
    for y in range(c.h):
        for x in range(c.w):
            v = rng.random()
            if v < pit:
                c.px(x, y, shade(base, 0.82))
            elif v < density * 0.5 + pit:
                c.px(x, y, light)
            elif v < density + pit:
                c.px(x, y, dark)
            else:
                c.px(x, y, base)
