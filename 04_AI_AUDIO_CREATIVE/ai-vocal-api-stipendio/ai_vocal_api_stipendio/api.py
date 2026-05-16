from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException

from .schemas import PredictRequest, PredictResponse, StatusResponse, TrainRequest, TrainResponse
from .service import SalaryPredictionService


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_PATH = PROJECT_ROOT / "data" / "synthetic_salary_profiles.csv"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "salary_classifier.json"

service = SalaryPredictionService(
    dataset_path=DEFAULT_DATASET_PATH,
    model_path=DEFAULT_MODEL_PATH,
)

app = FastAPI(
    title="AI Vocal API Stipendio",
    version="0.1.0",
    description=(
        "Educational synthetic salary-profile classifier. "
        "Not valid for real salary, employment, eligibility or financial decisions."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "warning": "synthetic educational project only",
    }


@app.get("/status", response_model=StatusResponse)
def status() -> dict[str, object]:
    return service.status()


@app.post("/train", response_model=TrainResponse)
def train(request: TrainRequest) -> TrainResponse:
    if request.regenerate_dataset:
        service.regenerate_dataset(samples=request.samples, seed=request.seed)

    result = service.train()
    return TrainResponse(**result.__dict__)


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> dict[str, object]:
    try:
        return service.predict(
            age=request.age,
            experience=request.experience,
            education_level=request.education_level,
            current_salary=request.current_salary,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/dataset")
def dataset_summary() -> dict[str, object]:
    return {
        "dataset_path": str(DEFAULT_DATASET_PATH),
        "dataset_size": service.dataset.size,
        "positive_rate": service.dataset.positive_rate,
        "feature_names": service.dataset.feature_names,
        "warning": "synthetic dataset only",
    }
