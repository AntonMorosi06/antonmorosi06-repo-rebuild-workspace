from __future__ import annotations

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    age: float = Field(..., ge=0, le=120)
    experience: float = Field(..., ge=0, le=80)
    education_level: float = Field(..., ge=1, le=5)
    current_salary: float = Field(..., ge=0, le=300000)


class PredictResponse(BaseModel):
    label: int
    probability: float
    class_name: str
    warnings: list[str]
    model_warning: str


class TrainRequest(BaseModel):
    regenerate_dataset: bool = False
    samples: int = Field(800, ge=20, le=20000)
    seed: int = 42


class TrainResponse(BaseModel):
    backend: str
    accuracy: float
    loss: float
    dataset_size: int
    positive_rate: float
    model_path: str


class StatusResponse(BaseModel):
    dataset_path: str
    model_path: str
    dataset_size: int
    positive_rate: float
    trained: bool
    metadata: dict
