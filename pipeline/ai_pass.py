"""Optional AI polish hook for the Game Asset Factory.

STATUS: OFF by default. The pipeline never calls any AI service and makes
no network requests. If an AI polish pass is ever wanted, a HUMAN must
explicitly take three steps:

  1. render the asset locally with the pipeline,
  2. supply its PNG path via --image or the GDAF_AI_POLISH_IMAGE env var,
  3. connect an external, human-gated service (not provided in this
     product) that reads that file.

HUMAN_GATE: nothing in this product makes API calls or spends money.
Any real AI pass requires explicit human approval before spend.
"""
from __future__ import annotations

import os

from PIL import Image


def run(image_path=None):
    path = image_path or os.environ.get("GDAF_AI_POLISH_IMAGE")
    if not path:
        print("[ai_pass] OFF: no image path supplied "
              "(use --image PATH or set GDAF_AI_POLISH_IMAGE).")
        print("[ai_pass] The AI polish pass is optional and disabled by default; "
              "no API calls were made, no money spent.")
        return 0

    if not os.path.isfile(path):
        print(f"[ai_pass] ERROR: file not found: {path}")
        return 2

    try:
        with Image.open(path) as im:
            im.verify()
    except Exception as exc:  # noqa: BLE001
        print(f"[ai_pass] ERROR: {path} is not a readable image: {exc}")
        return 2

    with Image.open(path) as im:
        print(f"[ai_pass] image accepted: {path} ({im.format}, {im.size[0]}x{im.size[1]})")

    print("[ai_pass] HUMAN_GATE: this hook made zero API calls. "
          "Any AI/service spend requires explicit human approval.")
    return 0
