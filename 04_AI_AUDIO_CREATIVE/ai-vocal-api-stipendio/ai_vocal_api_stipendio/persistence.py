from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any

from .model import LogisticSalaryClassifier
from .preprocessing import StandardScaler


@dataclass
class PersistedModel:
    model: LogisticSalaryClassifier
    scaler: StandardScaler
    metadata: dict[str, Any]


def save_model_bundle(
    path: Path,
    model: LogisticSalaryClassifier,
    scaler: StandardScaler,
    metadata: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "model": model.to_dict(),
        "scaler": scaler.to_dict(),
        "metadata": metadata,
    }

    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def load_model_bundle(path: Path) -> PersistedModel:
    if not path.exists():
        raise FileNotFoundError(f"model file not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))

    return PersistedModel(
        model=LogisticSalaryClassifier.from_dict(payload["model"]),
        scaler=StandardScaler.from_dict(payload["scaler"]),
        metadata=dict(payload.get("metadata", {})),
    )
