# Issue 001 - TensorFlow optional dependency

## Goal

Keep the repository runnable even when TensorFlow is not installed.

## Current implementation

The runtime checks whether TensorFlow is available. If it is available and the user prefers Keras, the app trains a small Keras classifier. Otherwise, it uses a NumPy logistic classifier.

## Acceptance criteria

Running python3 main.py should not require TensorFlow.

The README should explain optional Keras installation.

The app should display which backend was used.

The fallback should remain deterministic enough for testing and education.
