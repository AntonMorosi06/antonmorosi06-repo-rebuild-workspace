from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class StandardScaler:
    mean_: np.ndarray
    scale_: np.ndarray

    @classmethod
    def fit(cls, x: np.ndarray) -> "StandardScaler":
        x = np.asarray(x, dtype=float)
        if x.ndim != 2:
            raise ValueError("x must be a 2D matrix")

        mean = np.mean(x, axis=0)
        scale = np.std(x, axis=0)
        scale = np.where(scale > 1e-12, scale, 1.0)
        return cls(mean_=mean, scale_=scale)

    def transform(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        return (x - self.mean_) / self.scale_

    def fit_transform(cls, x: np.ndarray) -> np.ndarray:
        raise RuntimeError("Use StandardScaler.fit(x).transform(x) instead.")


def validate_profile(age: float, salary: float, experience: float) -> list[str]:
    warnings = []

    if age < 16 or age > 80:
        warnings.append("age is outside the educational training range")

    if salary < 8000 or salary > 180000:
        warnings.append("salary is outside the educational training range")

    if experience < 0:
        warnings.append("experience cannot realistically be negative")

    if experience > max(0.0, age - 14):
        warnings.append("experience is unusually high compared with age")

    return warnings


def profile_to_array(age: float, salary: float, experience: float) -> np.ndarray:
    return np.asarray([[float(age), float(salary), float(experience)]], dtype=float)
