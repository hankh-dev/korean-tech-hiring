from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIPELINE_DIR = ROOT / "pipeline"
BOARDS_PATH = PIPELINE_DIR / "boards.json"
NOTES_PATH = PIPELINE_DIR / "editor_notes.json"
HISTORY_DIR = PIPELINE_DIR / "history"
DEFAULT_OUT_DIR = ROOT / "web" / "data"


def load_boards() -> list[dict]:
    return json.loads(BOARDS_PATH.read_text(encoding="utf-8"))


def load_notes() -> dict[str, str]:
    if not NOTES_PATH.exists():
        return {}
    try:
        data = json.loads(NOTES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {str(k): str(v) for k, v in data.items() if v}
