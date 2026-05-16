from __future__ import annotations

from pathlib import Path
import json


def load_highscore(path: Path) -> int:
    if not path.exists():
        return 0

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return int(data.get("highscore", 0))
    except Exception:
        return 0


def save_highscore(path: Path, score: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"highscore": int(score)}, indent=2), encoding="utf-8")


def update_highscore(path: Path, score: int) -> int:
    current = load_highscore(path)
    if score > current:
        save_highscore(path, score)
        return score
    return current
