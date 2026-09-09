# Game Asset Factory

Deterministic 16x16 pixel-art packs: tilesets, characters, UI kits. Pure Python, no AI, no network, no spend.

2D pixel-art sibling of `asset-pack-factory` (https://github.com/MaximKonovalovDev/asset-pack-factory).

## Why

Small games need art that is cheap, legal, and repeatable. These generators draw
every pixel from a seeded script, so the same seed gives the same PNGs byte for
byte. No API keys, no generated-asset licensing fog, no surprises.

## What it does

- 4 themed tileset generators (grass/forest, cave, water, desert).
- 4 characters x 4 directions x 4-frame walk cycles = 64 indexed frames per sheet.
- UI kit: button states, 9-slice panels, frame, 11 icons.
- Every pack ships `assets/` (PNG + JSON indexes), `preview.png`, `manifest.json`
  (seed, license, byte sizes), and `itch-listing.txt`.
- `verify` checks every manifest: files exist with exact byte sizes.
- Optional AI-polish hook exists but is OFF: with no image path it prints OFF
  and exits. Nothing here spends money.

## Quick start

```bash
pip install -r requirements.txt        # Pillow only

python -m pipeline packs               # build all 3 sample packs
python -m pipeline packs --pack 1      # or just one
python -m pipeline verify              # check packs against manifests
```

Standalone themed tilesets:

```bash
python -m pipeline tiles --theme cave --seed 5 --out out/cave
```

All commands above were run clean on 2026-09-09 (Python 3.13, Pillow 12.3.0).

## Demo + proof numbers

Measured 2026-09-09, in this checkout:

- `packs`: pack-1 wrote 6 files, pack-2 wrote 4, pack-3 wrote 4.
- `verify`: all 3 packs OK, every file matches its manifest byte size.
- `tiles --theme cave --seed 5`: 8 tiles in `out/cave` (tiles.png + index + collision).
- Pack contents: 14 forest tiles + 16x12 scene + collision map; 64 character
  frames; UI kit with 11 icons. Seeds recorded (pack-1: seed 42).
- Rebuilds are byte-identical by design (SHA-256 match); no network code in repo.

## Project structure

```
pipeline/       # CLI + generators: tiles, characters, ui, ai_pass, pix, palette
packs/          # 3 sample packs, each: assets/ + preview.png + manifest.json + listing
pack-1-forest-tileset/   # 14 tiles, scene, collision map
pack-2-village-characters/  # 4 characters x 4 dirs x 4 frames
pack-3-fantasy-ui-kit/      # buttons, panels, frame, 11 icons
```

## Honest limits

- 16x16 pixel art only; 2D only, no 3D, no normal maps.
- No audio. Walk cycles are 4-frame loops, 4 directions, no diagonals.
- No engine exports: PNGs + JSON indexes, no Tiled/Unity/Godot/Aseprite files.
- Character variety is palette/hat-parameterized, not free-form.

## License

MIT — see `LICENSE`. The three shipped packs are MIT too (see each manifest),
so buyers can use them in commercial or free projects.

## Author

Maxim Konovalov — Haifa. Game assets + procedural pipelines.
