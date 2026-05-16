from pathlib import Path
import tempfile

import numpy as np

from ai_vocal_api_stipendio.dataset import generate_synthetic_salary_profiles, save_dataset_csv, load_dataset_csv
from ai_vocal_api_stipendio.model import LogisticSalaryClassifier
from ai_vocal_api_stipendio.preprocessing import StandardScaler
from ai_vocal_api_stipendio.service import SalaryPredictionService


def test_dataset_generation_shape():
    dataset = generate_synthetic_salary_profiles(samples=120, seed=123)

    assert dataset.x.shape == (120, 4)
    assert dataset.y.shape == (120,)
    assert 0.0 <= dataset.positive_rate <= 1.0


def test_dataset_roundtrip():
    dataset = generate_synthetic_salary_profiles(samples=60, seed=5)

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "salary.csv"
        save_dataset_csv(dataset, path)
        loaded = load_dataset_csv(path)

    assert loaded.x.shape == dataset.x.shape
    assert loaded.y.shape == dataset.y.shape


def test_model_trains_and_predicts():
    dataset = generate_synthetic_salary_profiles(samples=150, seed=8)
    scaler = StandardScaler.fit(dataset.x)
    x_scaled = scaler.transform(dataset.x)

    model = LogisticSalaryClassifier.create(feature_count=4, epochs=150)
    metrics = model.fit(x_scaled, dataset.y)
    probabilities = model.predict_proba(x_scaled[:5])

    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert probabilities.shape == (5,)
    assert np.all(probabilities >= 0.0)
    assert np.all(probabilities <= 1.0)


def test_service_train_and_predict():
    with tempfile.TemporaryDirectory() as tmp:
        dataset_path = Path(tmp) / "data.csv"
        model_path = Path(tmp) / "model.json"

        service = SalaryPredictionService(dataset_path=dataset_path, model_path=model_path)
        service.regenerate_dataset(samples=120, seed=42)
        result = service.train()
        prediction = service.predict(age=32, experience=8, education_level=3, current_salary=52000)

    assert result.dataset_size == 120
    assert "probability" in prediction
    assert "model_warning" in prediction
