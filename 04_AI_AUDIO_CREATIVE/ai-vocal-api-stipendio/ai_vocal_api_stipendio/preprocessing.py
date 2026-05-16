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

    def to_dict(self) -> dict[str, list[float]]:
        return {
            "mean": [float(value) for value in self.mean_],
            "scale": [float(value) for value in self.scale_],
        }

    @classmethod
    def from_dict(cls, data: dict[str, list[float]]) -> "StandardScaler":
        return cls(
            mean_=np.asarray(data["mean"], dtype=float),
            scale_=np.asarray(data["scale"], dtype=float),
        )


def profile_to_array(age: float, experience: float, education_level: float, current_salary: float) -> np.ndarray:
    return np.asarray([[float(age), float(experience), float(education_level), float(current_salary)]], dtype=float)


def validate_profile(age: float, experience: float, education_level: float, current_salary: float) -> list[str]:
    warnings = []

    if age < 16 or age > 80:
        warnings.append("age is outside the educational training range")

    if experience < 0:
        warnings.append("experience cannot realistically be negative")

    if experience > max(0.0, age - 14):
        warnings.append("experience is unusually high compared with age")

    if education_level < 1 or education_level > 5:
        warnings.append("education_level should be between 1 and 5 in this synthetic dataset")

    if current_salary < 8000 or current_salary > 200000:
        warnings.append("current_salary is outside the educational training range")

    return warnings
