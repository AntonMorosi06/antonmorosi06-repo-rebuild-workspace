from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .dataset import SalaryDataset, ensure_dataset, generate_synthetic_salary_profiles, save_dataset_csv
from .model import LogisticSalaryClassifier
from .persistence import load_model_bundle, save_model_bundle
from .preprocessing import StandardScaler, profile_to_array, validate_profile


@dataclass
class TrainResult:
    backend: str
    accuracy: float
    loss: float
    dataset_size: int
    positive_rate: float
    model_path: str


class SalaryPredictionService:
    def __init__(self, dataset_path: Path, model_path: Path) -> None:
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.dataset: SalaryDataset = ensure_dataset(dataset_path)
        self.model: LogisticSalaryClassifier | None = None
        self.scaler: StandardScaler | None = None
        self.metadata: dict[str, Any] = {}

        if model_path.exists():
            try:
                bundle = load_model_bundle(model_path)
                self.model = bundle.model
                self.scaler = bundle.scaler
                self.metadata = bundle.metadata
            except Exception:
                self.model = None
                self.scaler = None
                self.metadata = {}

    @property
    def is_trained(self) -> bool:
        return self.model is not None and self.scaler is not None

    def regenerate_dataset(self, samples: int = 800, seed: int = 42) -> SalaryDataset:
        self.dataset = generate_synthetic_salary_profiles(samples=samples, seed=seed)
        save_dataset_csv(self.dataset, self.dataset_path)
        self.model = None
        self.scaler = None
        self.metadata = {}
        return self.dataset

    def train(self) -> TrainResult:
        self.dataset = ensure_dataset(self.dataset_path)
        self.scaler = StandardScaler.fit(self.dataset.x)
        x_scaled = self.scaler.transform(self.dataset.x)

        self.model = LogisticSalaryClassifier.create(feature_count=x_scaled.shape[1])
        metrics = self.model.fit(x_scaled, self.dataset.y)

        self.metadata = {
            "backend": "numpy-logistic-regression",
            "dataset_size": self.dataset.size,
            "positive_rate": self.dataset.positive_rate,
            "feature_names": self.dataset.feature_names,
            "warning": "synthetic educational model only; not valid for real salary or employment decisions",
        }

        save_model_bundle(
            path=self.model_path,
            model=self.model,
            scaler=self.scaler,
            metadata=self.metadata,
        )

        return TrainResult(
            backend="numpy-logistic-regression",
            accuracy=float(metrics["accuracy"]),
            loss=float(metrics["loss"]),
            dataset_size=self.dataset.size,
            positive_rate=self.dataset.positive_rate,
            model_path=str(self.model_path),
        )

    def status(self) -> dict[str, object]:
        return {
            "dataset_path": str(self.dataset_path),
            "model_path": str(self.model_path),
            "dataset_size": self.dataset.size,
            "positive_rate": self.dataset.positive_rate,
            "trained": self.is_trained,
            "metadata": self.metadata,
        }

    def predict(
        self,
        age: float,
        experience: float,
        education_level: float,
        current_salary: float,
    ) -> dict[str, object]:
        if not self.is_trained:
            if self.model_path.exists():
                bundle = load_model_bundle(self.model_path)
                self.model = bundle.model
                self.scaler = bundle.scaler
                self.metadata = bundle.metadata
            else:
                raise RuntimeError("model is not trained. Run `python3 main.py train` before prediction.")

        assert self.model is not None
        assert self.scaler is not None

        raw = profile_to_array(age, experience, education_level, current_salary)
        scaled = self.scaler.transform(raw)

        probability = float(self.model.predict_proba(scaled)[0])
        label = int(probability >= 0.5)
        warnings = validate_profile(age, experience, education_level, current_salary)

        explanation = (
            "Positive synthetic class"
            if label == 1
            else "Negative synthetic class"
        )

        return {
            "label": label,
            "probability": probability,
            "class_name": explanation,
            "warnings": warnings,
            "model_warning": "synthetic educational prediction only; do not use for real decisions",
        }
