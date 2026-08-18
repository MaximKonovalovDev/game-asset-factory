"""Simple grid spritesheet packing (uniform 16x16 cells) + index building."""
from __future__ import annotations

import json

from PIL import Image


def pack_grid(items, cols=4, cell=16):
    """Paste items (ordered dict name -> Canvas) into a grid sheet.

    Returns (PIL image, index dict: name -> {col,row,x,y,w,h}).
    """
    names = list(items.keys())
    rows = (len(names) + cols - 1) // cols
    img = Image.new("RGBA", (cols * cell, rows * cell), (0, 0, 0, 0))
    index = {}
    for i, name in enumerate(names):
        col, row = i % cols, i // cols
        canvas = items[name]
        frame = canvas.to_image()
        if frame.size != (cell, cell):
            frame = frame.resize((cell, cell), Image.NEAREST)
        img.paste(frame, (col * cell, row * cell))
        index[name] = {"col": col, "row": row, "x": col * cell, "y": row * cell, "w": cell, "h": cell}
    return img, index


def save_image(img, path):
    img.save(path, "PNG")


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
