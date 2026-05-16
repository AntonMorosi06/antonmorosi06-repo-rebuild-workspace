from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math
import random

import numpy as np


FEATURE_NAMES = ["age", "experience", "education_level", "current_salary"]


@dataclass
class SalaryDataset:
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


def generate_synthetic_salary_profiles(samples: int = 800, seed: int = 42) -> SalaryDataset:
    if samples < 20:
        raise ValueError("samples must be at least 20")

    rng = random.Random(seed)
    rows = []
    labels = []

    for _ in range(samples):
        age = rng.uniform(18.0, 65.0)
        experience = max(0.0, min(age - 16.0, rng.gauss((age - 22.0) * 0.72, 4.8)))
        education_level = rng.choice([1, 2, 3, 4, 5])

        base_salary = 17000.0
        salary = (
            base_salary
            + experience * rng.uniform(1500.0, 2300.0)
            + education_level * rng.uniform(2500.0, 5200.0)
            + age * rng.uniform(120.0, 360.0)
            + rng.gauss(0.0, 9000.0)
        )
        current_salary = max(12000.0, min(160000.0, salary))

        score = (
            -6.30
            + 0.032 * age
            + 0.190 * experience
            + 0.420 * education_level
            + 0.000030 * current_salary
            - 0.0012 * max(0.0, age - 55.0) ** 2
        )
        probability = sigmoid(score)
        noisy_probability = max(0.03, min(0.97, probability + rng.gauss(0.0, 0.060)))
        label = 1 if rng.random() < noisy_probability else 0

        rows.append([age, experience, education_level, current_salary])
        labels.append(label)

    return SalaryDataset(
        x=np.asarray(rows, dtype=float),
        y=np.asarray(labels, dtype=int),
        feature_names=list(FEATURE_NAMES),
    )


def save_dataset_csv(dataset: SalaryDataset, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(dataset.feature_names + ["target"])
        for features, label in zip(dataset.x, dataset.y):
            writer.writerow([round(float(value), 4) for value in features] + [int(label)])


def load_dataset_csv(path: Path) -> SalaryDataset:
    rows = []
    labels = []

    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append([
                float(row["age"]),
                float(row["experience"]),
                float(row["education_level"]),
                float(row["current_salary"]),
            ])
            labels.append(int(row["target"]))

    return SalaryDataset(
        x=np.asarray(rows, dtype=float),
        y=np.asarray(labels, dtype=int),
        feature_names=list(FEATURE_NAMES),
    )


def ensure_dataset(path: Path, samples: int = 800, seed: int = 42) -> SalaryDataset:
    if path.exists():
        return load_dataset_csv(path)

    dataset = generate_synthetic_salary_profiles(samples=samples, seed=seed)
    save_dataset_csv(dataset, path)
    return dataset
