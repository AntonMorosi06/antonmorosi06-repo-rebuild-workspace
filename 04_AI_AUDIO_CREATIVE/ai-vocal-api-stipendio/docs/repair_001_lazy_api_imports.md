# Repair 001 - Lazy API imports for CLI stability

## Problem

The first reconstructed batch imported `uvicorn` and the FastAPI app at the top of `cli.py`.

This caused even non-API commands such as `train`, `predict`, `status` and `generate-data` to fail when `uvicorn` was not installed.

## Fix

The API imports were moved inside `cmd_serve`.

Now the core CLI workflow can run without importing FastAPI or uvicorn.

The API dependencies are required only when running:

python3 main.py serve

## Expected behavior

python3 main.py train should work with the core project files.

python3 main.py predict should work after training.

python3 main.py serve should ask for API dependencies if they are missing.
