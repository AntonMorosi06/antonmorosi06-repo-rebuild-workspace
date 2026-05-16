from __future__ import annotations

from typing import Any

import numpy as np


def has_tensorflow() -> bool:
    try:
        import tensorflow  # noqa: F401
        return True
    except Exception:
        return False


def build_keras_model(input_dim: int) -> Any:
    try:
        from tensorflow import keras
    except Exception as exc:
        raise RuntimeError("TensorFlow/Keras is not installed. Install requirements-optional-keras.txt to use this backend.") from exc

    model = keras.Sequential(
        [
            keras.layers.Input(shape=(input_dim,)),
            keras.layers.Dense(16, activation="relu"),
            keras.layers.Dense(8, activation="relu"),
            keras.layers.Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.01),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train_keras_classifier(x: np.ndarray, y: np.ndarray, epochs: int = 35) -> tuple[Any, dict[str, float]]:
    model = build_keras_model(input_dim=x.shape[1])
    history = model.fit(x, y, epochs=epochs, batch_size=32, verbose=0)
    metrics = {
        "accuracy": float(history.history.get("accuracy", [0.0])[-1]),
        "loss": float(history.history.get("loss", [0.0])[-1]),
    }
    return model, metrics


def keras_predict_probability(model: Any, x: np.ndarray) -> float:
    prediction = model.predict(x, verbose=0)
    return float(prediction.reshape(-1)[0])
