# Train before predict

This repository intentionally separates training and prediction.

A prediction should not silently train a model in production-style API behavior, because that can hide important state changes. Instead, the API reports an error if the model is not trained.

Recommended workflow:

Generate the synthetic dataset.

Train the model.

Check status.

Run predictions.

CLI example:

python3 main.py generate-data
python3 main.py train
python3 main.py status
python3 main.py predict --age 32 --experience 8 --education-level 3 --current-salary 52000

API example:

POST /train

POST /predict

This explicit workflow makes demos clearer and reduces confusion when the model file is missing.
