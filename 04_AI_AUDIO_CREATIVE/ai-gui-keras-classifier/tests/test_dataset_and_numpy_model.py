from pathlib import Path
import tempfile

import numpy as np

from ai_gui_keras_classifier.dataset import generate_synthetic_profiles, load_dataset_csv, save_dataset_csv
from ai_gui_keras_classifier.numpy_classifier import NumpyLogisticClassifier
from ai_gui_keras_classifier.preprocessing import StandardScaler, validate_profile


def test_dataset_generation_shape():
    dataset = generate_synthetic_profiles(samples=120, seed=123)

    assert dataset.x.shape == (120, 3)
    assert dataset.y.shape == (120,)
    assert 0.0 <= dataset.positive_rate <= 1.0


def test_dataset_save_and_load_roundtrip():
    dataset = generate_synthetic_profiles(samples=50, seed=7)

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "profiles.csv"
        save_dataset_csv(dataset, path)
        loaded = load_dataset_csv(path)

    assert loaded.x.shape == dataset.x.shape
    assert loaded.y.shape == dataset.y.shape


def test_numpy_classifier_trains_and_predicts():
    dataset = generate_synthetic_profiles(samples=160, seed=21)
    scaler = StandardScaler.fit(dataset.x)
    x_scaled = scaler.transform(dataset.x)

    model = NumpyLogisticClassifier.create(feature_count=3, epochs=120)
    metrics = model.fit(x_scaled, dataset.y)

    probabilities = model.predict_proba(x_scaled[:5])

    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert probabilities.shape == (5,)
    assert np.all(probabilities >= 0.0)
    assert np.all(probabilities <= 1.0)


def test_validation_warning_for_negative_experience():
    warnings = validate_profile(age=20, salary=25000, experience=-1)

    assert warnings
