# Game Asset Factory

A small factory that produces **16x16 pixel-art asset packs** (tilesets,
character sheets, UI kits) fully **procedurally** — every pixel is drawn by
seeded generators in pure Python (stdlib + Pillow). No AI, no API keys, no
network, no spend. Same seed in, same PNGs out, byte for byte.

- **Deterministic** — every pack has an integer seed; regeneration is
  reproducible and verified against the manifest.
- **No heavy deps** — Python 3.9+ and Pillow only.
- **AI polish is optional and OFF by default** (see below).

## Layout

```
game-asset-factory/
├── pipeline/            # the factory: CLI + generators
│   ├── cli.py           #   commands: packs, tiles, ai-pass, verify
│   ├── tiles.py         #   tileset generators (grass/cave/water/desert)
│   ├── characters.py    #   4 characters x 4 directions x 4-frame walk cycles
│   ├── ui.py            #   buttons, 9-slice panels, icons
│   ├── ai_pass.py       #   optional AI polish hook (OFF, no API calls)
│   └── pix.py, palette.py, spritesheet.py
├── packs/               # three ready-made sample packs
│   ├── pack-1-forest-tileset/
│   ├── pack-2-village-characters/
│   └── pack-3-fantasy-ui-kit/
├── requirements.txt
└── README.md
```

## Quick start

```bash
pip install -r requirements.txt        # Pillow only

python -m pipeline packs               # build all 3 sample packs
python -m pipeline packs --pack 1      # or just one
python -m pipeline verify              # check packs against their manifests
```

Standalone themed tilesets (not shipped as packs, available for re-use):

```bash
python -m pipeline tiles --theme cave   --seed 5 --out out/cave
python -m pipeline tiles --theme water  --seed 5 --out out/water
python -m pipeline tiles --theme desert --seed 5 --out out/desert
```

## What a pack contains

Every pack ships `assets/` (PNG spritesheets + JSON index files),
`preview.png` (an actual rendered preview), `manifest.json` (theme, seed,
license, file list with byte sizes) and `itch-listing.txt` (3-line listing
blurb, no invented claims).

| Pack | Contents |
| --- | --- |
| **pack-1-forest-tileset** | 14 tiles (grass, flowers, tufts, dirt, path, tree, rock, bush, bridge + 4-frame animated water), an assembled 16x12 scene, and a 16x12 collision map (0 = walkable, 1 = solid) |
| **pack-2-village-characters** | 4 characters (Knight, Villager, Wizard, Merchant) x 4 directions x 4 walk frames = 64 indexed frames in one sheet |
| **pack-3-fantasy-ui-kit** | 3 button states, a 9-slice panel set (2px border: 4 corners, 4 stretchable edges, center), a frame, and 11 icons (heart, coin, sword, shield, key, potion, star, chest, gem, map, crown) |

All spritesheets are 16x16-cell RGBA PNGs with per-tile/per-frame index
JSONs (`tiles_index.json`, `characters_index.json`, `ui_index.json`).

## The AI polish pass — OFF by default

`python -m pipeline ai-pass` is a **hook point**, not a service:

- It does **not** call any AI, makes **zero API requests**, and reads at
  most a single PNG path you pass explicitly
  (`--image path.png` or `GDAF_AI_POLISH_IMAGE`).
- With no path it prints `OFF` and exits.
- Any real AI polish would require a human to connect an external,
  human-gated service to that file. **HUMAN_GATE**: nothing in this
  product spends money; API spend requires explicit human approval.

## License & attribution

All code here is **MIT** — original, written fresh for this factory
(see `LICENSE`). No art, code or assets were copied from the reference
repos; they were studied for approach only:

| Repo | License | Role |
| --- | --- | --- |
| [KilledByAPixel/ZzSprite](https://github.com/KilledByAPixel/ZzSprite) | MIT | inspiration for procedural sprite techniques |
| [kase1111-hash/Tile-Crawler](https://github.com/kase1111-hash/Tile-Crawler) | MIT | tileset organization approach |
| [IsaacJCarnes/TilesetViewer](https://github.com/IsaacJCarnes/TilesetViewer) | **no license** | conceptual tileset-tooling reference only; nothing used |
| [draeton/stitches](https://github.com/draeton/stitches) | MIT | spritesheet packing concept (we use simple uniform grid packing) |

The three shipped packs are licensed **MIT** (see each `manifest.json`),
so buyers can use them in commercial or free projects.

## Verification & determinism

- `python -m pipeline verify` re-reads each manifest and confirms every
  listed file exists with the exact recorded byte size, plus valid
  `preview.png` and `itch-listing.txt`.
- A clean rebuild (`rm -rf packs && python -m pipeline packs`) is
  **byte-identical**: SHA-256 hashes match on every file.
- The product contains no API keys, no URLs, and no network code.

## GAP report (honest limits)

- **16x16 pixel art only** — no larger resolutions, no tilesets > 16px.
- **2D only** — no 3D models, meshes or normal maps; AI-realism is out of
  scope by design.
- **No audio**, no skeletal/rigged animation (walk cycles are simple
  4-frame pixel loops; 4 directions, no diagonals).
- **No engine-specific exports** — no Tiled `.tsx`, Unity `.meta`,
  Godot `.tres`, or Aseprite files. Consumers get PNGs + JSON indexes.
- Character variety is palette/hat-parameterized, not free-form.

