"""Command-line interface: build the sample packs, standalone tilesets,
the AI polish hook, and a verifier that checks packs against manifests."""
from __future__ import annotations

import argparse
import json
import os
import random
import sys

from . import __version__
from .ai_pass import run as ai_pass_run
from .characters import DIRS, make_all_characters
from .pix import hash_seed
from .spritesheet import pack_grid, save_image, write_json
from .tiles import make_tiles
from .ui import NINE_SLICE, make_ui_kit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS_DIR = os.path.join(ROOT, "packs")
TILE = 16

PACKS = [
    {
        "num": 1, "dir": "pack-1-forest-tileset", "title": "Forest Tileset",
        "theme": "grass", "seed": 42,
        "notes": [
            "Animated water is 4 frames (water_0..water_3); cycle at ~6 fps.",
            "collision_map.json: 16x12 grid, 0 = walkable, 1 = solid.",
            "tiles.png: 7 columns per row; tiles_index.json maps every tile.",
        ],
        "listing": [
            "Forest Tileset: 16x16 pixel-art tiles with animated water, trees, rocks and a dirt path, plus a ready-to-use collision map.",
            "Every tile is indexed and named in manifest.json - paste the sheet into any engine and use the map as-is.",
            "MIT licensed and generated deterministically by the Game Asset Factory; re-roll with a new seed anytime.",
        ],
    },
    {
        "num": 2, "dir": "pack-2-village-characters", "title": "Village Characters",
        "theme": "none", "seed": 1337,
        "notes": [
            "4 characters x 4 directions (down, left, right, up) x 4 walk frames = 64 frames.",
            "characters.png rows: character blocks (4 direction rows each); cols: frames 0-3.",
            "characters_index.json maps every character, direction and frame to its cell.",
        ],
        "listing": [
            "Village Characters: four 16x16 pixel characters (knight, villager, wizard, merchant) with 4-frame walk cycles in all four directions.",
            "One cleanly indexed spritesheet - 64 frames total, every cell mapped in the manifest.",
            "MIT licensed, procedurally generated with deterministic seeds, and ready for any engine.",
        ],
    },
    {
        "num": 3, "dir": "pack-3-fantasy-ui-kit", "title": "Fantasy UI Kit",
        "theme": "none", "seed": 9001,
        "notes": [
            "ui.png: 4 columns x 6 rows. Buttons (3 states), frame, 9-slice panel pieces, 11 icons.",
            "9-slice: 2px border; corners are 16x16, edges stretch, center tiles (see manifest nine_slice).",
            "preview.png shows an assembled panel + buttons + icons at 4x scale.",
        ],
        "listing": [
            "Fantasy UI Kit: buttons, panels and icons in crisp 16x16 pixel art, with 9-slice corner data included.",
            "Three button states, a full nine-slice panel set, and eleven game-ready icons in one indexed sheet.",
            "MIT licensed and generated procedurally - recolor or re-slice to fit your game.",
        ],
    },
]


def _manifest(meta):
    data = {
        "product": "GD-L3 Game Asset Factory",
        "pipeline_version": __version__,
        "pack_id": meta["dir"],
        "title": meta["title"],
        "license": "MIT",
        "generated_by": "procedural generators (seeded); no AI, no API calls, no network",
        "seed": meta["seed"],
        "tile_size": TILE,
        "notes": meta["notes"],
        "regenerate": f"python -m pipeline packs --pack {meta['num']}",
        "contents": {},
    }
    return data


def _add_contents(manifest, pack_dir):
    for root, _dirs, files in os.walk(pack_dir):
        for name in sorted(files):
            if name == "manifest.json":
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, pack_dir).replace("\\", "/")
            manifest["contents"][rel] = os.path.getsize(full)


# ----------------------------------------------------------------- pack 1 --

def _forest_scene(tiles, meta, seed):
    rng = random.Random(hash_seed(seed, "forest_scene"))
    names = list(tiles.keys())
    grid = [["grass"] * 16 for _ in range(12)]

    def place(name, n, y0, y1):
        for _ in range(n):
            x, y = rng.randrange(1, 15), rng.randrange(y0, y1)
            grid[y][x] = name

    place("tree", 6, 1, 9)
    place("rock", 3, 1, 9)
    place("bush", 2, 1, 9)
    for _ in range(8):
        x, y = rng.randrange(0, 16), rng.randrange(0, 10)
        if grid[y][x] == "grass":
            grid[y][x] = "grass_tuft" if rng.random() < 0.6 else "grass_flower"

    for x in range(16):
        grid[10][x] = "path"
    for x in range(16):
        grid[11][x] = f"water_{x % 4}"
    for x in (6, 7, 8):
        grid[11][x] = "bridge"

    coll = meta["collision"]
    collision = [[coll[grid[y][x]] for x in range(16)] for y in range(12)]

    from .pix import Canvas
    canvas = Canvas(16 * TILE, 12 * TILE, bg=(42, 74, 30))
    for y in range(12):
        for x in range(16):
            tile_canvas = tiles[grid[y][x]]
            src = tile_canvas.to_image()
            canvas = _paste(canvas, src, x * TILE, y * TILE)
    return canvas, collision


def _paste(canvas, pil_src, ox, oy):
    for y in range(pil_src.height):
        for x in range(pil_src.width):
            r, g, b, a = pil_src.getpixel((x, y))
            if a:
                canvas.px(ox + x, oy + y, (r, g, b))
    return canvas


def _build_pack1(pack):
    seed = pack["seed"]
    tiles, meta = make_tiles("grass", seed)
    sheet, index = pack_grid(tiles, cols=7)
    assets = os.path.join(PACKS_DIR, pack["dir"], "assets")
    os.makedirs(assets, exist_ok=True)
    save_image(sheet, os.path.join(assets, "tiles.png"))
    write_json(os.path.join(assets, "tiles_index.json"), {
        "theme": "grass", "tile_size": TILE,
        "sheet": "tiles.png", "collision_per_tile": meta["collision"],
        "tiles": index,
    })

    scene_canvas, collision = _forest_scene(tiles, meta, seed)
    scene_img = scene_canvas.to_image()
    save_image(scene_img, os.path.join(assets, "scene.png"))
    write_json(os.path.join(assets, "collision_map.json"), {
        "cols": 16, "rows": 12, "tile_size": TILE,
        "legend": "0 = walkable, 1 = solid", "grid": collision,
    })

    preview = scene_img.resize((16 * 4, 12 * 4), __import__("PIL").Image.NEAREST)
    save_image(preview, os.path.join(PACKS_DIR, pack["dir"], "preview.png"))


# ----------------------------------------------------------------- pack 2 --

def _build_pack2(pack):
    seed = pack["seed"]
    chars = make_all_characters(seed)
    items = {}
    for spec, char in chars:
        for d in DIRS:
            for f, canvas in enumerate(char[d]):
                items[f"{spec['id']}_{d}_{f}"] = canvas
    sheet, index = pack_grid(items, cols=4)
    assets = os.path.join(PACKS_DIR, pack["dir"], "assets")
    os.makedirs(assets, exist_ok=True)
    save_image(sheet, os.path.join(assets, "characters.png"))

    char_index = {}
    for spec, _char in chars:
        char_index[spec["id"]] = {"name": spec["name"]}
        for d in DIRS:
            char_index[spec["id"]][d] = {
                str(f): index[f"{spec['id']}_{d}_{f}"] for f in range(4)
            }
    write_json(os.path.join(assets, "characters_index.json"), {
        "tile_size": TILE, "sheet": "characters.png",
        "rows_per_character": 4, "direction_order": list(DIRS),
        "characters": char_index,
    })

    tiles, _meta = make_tiles("grass", seed)
    bg = tiles["grass"].to_image()
    from PIL import Image
    img = Image.new("RGBA", (6 * TILE, 2 * TILE), (0, 0, 0, 0))
    for y in range(2):
        for x in range(6):
            img.paste(bg, (x * TILE, y * TILE))
    for i, (spec, char) in enumerate(chars):
        src = char["down"][0].to_image()
        img.paste(src, (8 + i * 20, 8), src)
    preview = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
    save_image(preview, os.path.join(PACKS_DIR, pack["dir"], "preview.png"))


# ----------------------------------------------------------------- pack 3 --

def _assemble_panel(items, w, h):
    from PIL import Image
    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    c = TILE
    corners = ["panel_corner_tl", "panel_corner_tr", "panel_corner_bl", "panel_corner_br"]
    positions = [(0, 0), (w - c, 0), (0, h - c), (w - c, h - c)]
    for name, (px, py) in zip(corners, positions):
        panel.paste(items[name].to_image(), (px, py))
    panel.paste(items["panel_edge_top"].to_image().resize((w - 2 * c, c), 0), (c, 0))
    panel.paste(items["panel_edge_bottom"].to_image().resize((w - 2 * c, c), 0), (c, h - c))
    panel.paste(items["panel_edge_left"].to_image().resize((c, h - 2 * c), 0), (0, c))
    panel.paste(items["panel_edge_right"].to_image().resize((c, h - 2 * c), 0), (w - c, c))
    panel.paste(items["panel_center"].to_image().resize((w - 2 * c, h - 2 * c), 0), (c, c))
    return panel


def _build_pack3(pack):
    seed = pack["seed"]
    items = make_ui_kit(seed)
    sheet, index = pack_grid(items, cols=4)
    assets = os.path.join(PACKS_DIR, pack["dir"], "assets")
    os.makedirs(assets, exist_ok=True)
    save_image(sheet, os.path.join(assets, "ui.png"))
    write_json(os.path.join(assets, "ui_index.json"), {
        "tile_size": TILE, "sheet": "ui.png",
        "elements": index,
        "nine_slice": NINE_SLICE,
        "button_states": ["button_normal", "button_hover", "button_pressed"],
    })

    from PIL import Image
    W, H = 96, 124
    img = Image.new("RGBA", (W, H), (30, 26, 44))
    panel = _assemble_panel(items, 56, 40)
    img.paste(panel, (4, 4))
    for x, name in zip((8, 40, 72), ("button_normal", "button_hover", "button_pressed")):
        src = items[name].to_image()
        img.paste(src, (x, 48), src)
    src = items["frame"].to_image()
    img.paste(src, (8, 68), src)
    icon_names = [n for n in items if n.startswith("icon_")]
    for i, name in enumerate(icon_names[:6]):
        src = items[name].to_image()
        img.paste(src, (i * 16, 88), src)
    for i, name in enumerate(icon_names[6:]):
        src = items[name].to_image()
        img.paste(src, (i * 16, 108), src)
    preview = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
    save_image(preview, os.path.join(PACKS_DIR, pack["dir"], "preview.png"))


# ------------------------------------------------------------------ cli ----

_BUILDERS = {1: _build_pack1, 2: _build_pack2, 3: _build_pack3}


def cmd_packs(args):
    targets = [p for p in PACKS if args.pack in (None, p["num"])]
    for pack in targets:
        pack_dir = os.path.join(PACKS_DIR, pack["dir"])
        os.makedirs(pack_dir, exist_ok=True)
        _BUILDERS[pack["num"]](pack)
        with open(os.path.join(pack_dir, "itch-listing.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(pack["listing"]) + "\n")
        manifest = _manifest(pack)
        _add_contents(manifest, pack_dir)
        write_json(os.path.join(pack_dir, "manifest.json"), manifest)
        print(f"[packs] {pack['dir']}: {len(manifest['contents'])} files written")
    return 0


def cmd_tiles(args):
    tiles, meta = make_tiles(args.theme, args.seed)
    os.makedirs(args.out, exist_ok=True)
    sheet, index = pack_grid(tiles, cols=7)
    save_image(sheet, os.path.join(args.out, "tiles.png"))
    write_json(os.path.join(args.out, "tiles_index.json"), {
        "theme": args.theme, "seed": args.seed, "tile_size": TILE,
        "collision_per_tile": meta["collision"], "tiles": index,
    })
    write_json(os.path.join(args.out, "collision.json"), {
        "theme": args.theme, "seed": args.seed,
        "collision_per_tile": meta["collision"],
        "solid_count": sum(meta["collision"].values()),
    })
    print(f"[tiles] theme={args.theme} seed={args.seed} -> "
          f"{len(tiles)} tiles in {args.out}")
    return 0


def cmd_verify(args):  # noqa: ARG001
    failures = 0
    for pack in PACKS:
        pack_dir = os.path.join(PACKS_DIR, pack["dir"])
        mf = os.path.join(pack_dir, "manifest.json")
        if not os.path.isfile(mf):
            print(f"[verify] FAIL {pack['dir']}: missing manifest.json")
            failures += 1
            continue
        with open(mf, encoding="utf-8") as fh:
            manifest = json.load(fh)
        errors = []
        for rel, size in manifest.get("contents", {}).items():
            full = os.path.join(pack_dir, rel)
            if not os.path.isfile(full):
                errors.append(f"missing {rel}")
            elif os.path.getsize(full) != size:
                errors.append(f"size mismatch {rel}")
        for extra in ("preview.png", "itch-listing.txt"):
            if not os.path.isfile(os.path.join(pack_dir, extra)):
                errors.append(f"missing {extra}")
        if errors:
            failures += 1
            print(f"[verify] FAIL {pack['dir']}: " + "; ".join(errors))
        else:
            print(f"[verify] OK {pack['dir']}: {len(manifest['contents'])} files match manifest")
    return 1 if failures else 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="pipeline",
        description=f"GD-L3 Game Asset Factory v{__version__} - procedural 16x16 pixel-art packs. "
                    "No AI, no API calls, no network. Deterministic seeds.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("packs", help="Generate the three sample packs into packs/")
    p.add_argument("--pack", type=int, choices=(1, 2, 3), default=None,
                   help="regenerate only one pack (default: all)")

    p = sub.add_parser("tiles", help="Generate a standalone themed tileset")
    p.add_argument("--theme", required=True, choices=("grass", "cave", "water", "desert"))
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--out", required=True, help="output directory")

    p = sub.add_parser("ai-pass", help="Optional AI polish hook (OFF by default, no API calls)")
    p.add_argument("--image", default=None, help="path to an existing PNG")

    sub.add_parser("verify", help="Check packs/ against manifests")

    args = ap.parse_args(argv)
    if args.cmd == "packs":
        return cmd_packs(args)
    if args.cmd == "tiles":
        return cmd_tiles(args)
    if args.cmd == "ai-pass":
        return ai_pass_run(args.image)
    if args.cmd == "verify":
        return cmd_verify(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
