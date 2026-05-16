from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from .dataset import SyntheticDataset, ensure_default_dataset, generate_synthetic_profiles, save_dataset_csv
from .keras_model import has_tensorflow, keras_predict_probability, train_keras_classifier
from .numpy_classifier import NumpyLogisticClassifier
from .preprocessing import StandardScaler, profile_to_array, validate_profile


@dataclass
class TrainingResult:
    backend: str
    accuracy: float
    loss: float
    dataset_size: int
    positive_rate: float


class ClassifierRuntime:
    def __init__(self, dataset_path: Path) -> None:
        self.dataset_path = dataset_path
        self.dataset: SyntheticDataset = ensure_default_dataset(dataset_path)
        self.scaler: StandardScaler | None = None
        self.backend: str = "untrained"
        self.model: Any = None
        self.last_training: TrainingResult | None = None

    def regenerate_dataset(self, samples: int = 600, seed: int = 42) -> SyntheticDataset:
        self.dataset = generate_synthetic_profiles(samples=samples, seed=seed)
        save_dataset_csv(self.dataset, self.dataset_path)
        self.scaler = None
        self.model = None
        self.backend = "untrained"
        self.last_training = None
        return self.dataset

    def train(self, prefer_keras: bool = True) -> TrainingResult:
        self.scaler = StandardScaler.fit(self.dataset.x)
        x_scaled = self.scaler.transform(self.dataset.x)
        y = self.dataset.y

        if prefer_keras and has_tensorflow():
            keras_model, metrics = train_keras_classifier(x_scaled, y)
            self.model = keras_model
            self.backend = "keras"
        else:
            model = NumpyLogisticClassifier.create(feature_count=x_scaled.shape[1])
            metrics = model.fit(x_scaled, y)
            self.model = model
            self.backend = "numpy-logistic-fallback"

        result = TrainingResult(
            backend=self.backend,
            accuracy=float(metrics["accuracy"]),
            loss=float(metrics["loss"]),
            dataset_size=self.dataset.size,
            positive_rate=self.dataset.positive_rate,
        )
        self.last_training = result
        return result

    def predict(self, age: float, salary: float, experience: float) -> dict[str, object]:
        if self.model is None or self.scaler is None:
            self.train(prefer_keras=True)

        assert self.scaler is not None
        assert self.model is not None

        raw = profile_to_array(age, salary, experience)
        scaled = self.scaler.transform(raw)

        if self.backend == "keras":
            probability = keras_predict_probability(self.model, scaled)
        else:
            probability = float(self.model.predict_proba(scaled)[0])

        label = int(probability >= 0.5)
        warnings = validate_profile(age, salary, experience)

        return {
            "label": label,
            "probability": probability,
            "backend": self.backend,
            "warnings": warnings,
        }
