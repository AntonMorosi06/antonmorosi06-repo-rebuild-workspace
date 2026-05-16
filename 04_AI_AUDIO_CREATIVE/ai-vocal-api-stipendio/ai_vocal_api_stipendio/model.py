from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


@dataclass
class LogisticSalaryClassifier:
    weights: np.ndarray
    bias: float
    learning_rate: float = 0.075
    epochs: int = 900

    @classmethod
    def create(cls, feature_count: int, learning_rate: float = 0.075, epochs: int = 900) -> "LogisticSalaryClassifier":
        return cls(
            weights=np.zeros(feature_count, dtype=float),
            bias=0.0,
            learning_rate=learning_rate,
            epochs=epochs,
        )

    def fit(self, x: np.ndarray, y: np.ndarray) -> dict[str, float]:
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if x.ndim != 2:
            raise ValueError("x must be a 2D matrix")
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        if x.shape[1] != len(self.weights):
            raise ValueError("feature count does not match model weights")

        n = max(1, len(y))

        for _ in range(self.epochs):
            logits = x @ self.weights + self.bias
            probabilities = sigmoid(logits)
            error = probabilities - y

            grad_w = (x.T @ error) / n
            grad_b = float(np.mean(error))

            self.weights -= self.learning_rate * grad_w
            self.bias -= self.learning_rate * grad_b

        probabilities = self.predict_proba(x)
        labels = (probabilities >= 0.5).astype(int)

        accuracy = float(np.mean(labels == y))
        loss = float(
            -np.mean(
                y * np.log(probabilities + 1e-9)
                + (1.0 - y) * np.log(1.0 - probabilities + 1e-9)
            )
        )

        return {
            "accuracy": accuracy,
            "loss": loss,
        }

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        return sigmoid(x @ self.weights + self.bias)

    def predict(self, x: np.ndarray) -> np.ndarray:
        return (self.predict_proba(x) >= 0.5).astype(int)

    def to_dict(self) -> dict[str, object]:
        return {
            "weights": [float(value) for value in self.weights],
            "bias": float(self.bias),
            "learning_rate": float(self.learning_rate),
            "epochs": int(self.epochs),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "LogisticSalaryClassifier":
        return cls(
            weights=np.asarray(data["weights"], dtype=float),
            bias=float(data["bias"]),
            learning_rate=float(data.get("learning_rate", 0.075)),
            epochs=int(data.get("epochs", 900)),
        )
