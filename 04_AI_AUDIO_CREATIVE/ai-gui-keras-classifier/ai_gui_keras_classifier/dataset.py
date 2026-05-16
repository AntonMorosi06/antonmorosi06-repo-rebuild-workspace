from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math
import random
from typing import Iterable

import numpy as np


FEATURE_NAMES = ["age", "salary", "experience"]


@dataclass
class SyntheticDataset:
    x: np.ndarray
    y: np.ndarray
    feature_names: list[str]

    @property
    def size(self) -> int:
        return int(len(self.y))

    @property
    def positive_rate(self) -> float:
        if len(self.y) == 0:
            return 0.0
        return float(np.mean(self.y))


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def generate_synthetic_profiles(samples: int = 600, seed: int = 42) -> SyntheticDataset:
    if samples < 10:
        raise ValueError("samples must be at least 10")

    rng = random.Random(seed)
    rows = []
    labels = []

    for _ in range(samples):
        age = rng.uniform(18.0, 65.0)
        experience = max(0.0, min(age - 16.0, rng.gauss((age - 22.0) * 0.72, 4.5)))
        salary = rng.gauss(21000.0 + experience * 1850.0 + age * 280.0, 8500.0)
        salary = max(12000.0, min(145000.0, salary))

        score = (
            -5.20
            + 0.050 * age
            + 0.000035 * salary
            + 0.165 * experience
            - 0.0018 * max(0.0, age - 52.0) ** 2
        )
        probability = sigmoid(score)
        noisy_probability = min(0.97, max(0.03, probability + rng.gauss(0.0, 0.055)))
        label = 1 if rng.random() < noisy_probability else 0

        rows.append([age, salary, experience])
        labels.append(label)

    return SyntheticDataset(
        x=np.asarray(rows, dtype=float),
        y=np.asarray(labels, dtype=int),
        feature_names=list(FEATURE_NAMES),
    )


def save_dataset_csv(dataset: SyntheticDataset, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(dataset.feature_names + ["target"])
        for features, label in zip(dataset.x, dataset.y):
            writer.writerow([round(float(value), 4) for value in features] + [int(label)])


def load_dataset_csv(path: Path) -> SyntheticDataset:
    rows = []
    labels = []

    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append([
                float(row["age"]),
                float(row["salary"]),
                float(row["experience"]),
            ])
            labels.append(int(row["target"]))

    return SyntheticDataset(
        x=np.asarray(rows, dtype=float),
        y=np.asarray(labels, dtype=int),
        feature_names=list(FEATURE_NAMES),
    )


def ensure_default_dataset(path: Path, samples: int = 600, seed: int = 42) -> SyntheticDataset:
    if path.exists():
        return load_dataset_csv(path)

    dataset = generate_synthetic_profiles(samples=samples, seed=seed)
    save_dataset_csv(dataset, path)
    return dataset
