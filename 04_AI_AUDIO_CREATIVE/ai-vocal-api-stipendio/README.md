# AI Vocal API Stipendio

This repository is a clean reconstructed skeleton of the old AI vocal API stipendio project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project demonstrates a small educational machine learning API around a synthetic salary-related classification task. It includes a command-line interface, a FastAPI backend, a NumPy logistic regression model, dataset generation, model persistence, validation checks, curl examples, an optional voice/TTS helper layer and responsible documentation.

The goal is not to predict real salaries or evaluate real people. The dataset is synthetic. The labels are generated from an artificial rule. The model is useful for learning API structure, training-before-prediction workflow, request validation, model cards, privacy notes and local ML application design.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Main interface: CLI and FastAPI  
Model type: NumPy logistic regression  
Dataset type: synthetic educational salary profile data  
Voice support: optional helper layer  
Production claim: none  
Portfolio readiness: prepared baseline  

## Important warning

This project must not be used for real hiring, compensation, credit, eligibility, financial, educational, medical, legal or employment decisions. It is a toy educational classifier trained on synthetic data.

The word stipendio is used because the original project idea was connected to age, experience and salary examples. In this reconstructed version, that idea is treated carefully as an educational API only.

## Features

The project includes a synthetic dataset generator, feature scaling, a logistic regression model written with NumPy, JSON model persistence, a CLI, a FastAPI application, train and predict endpoints, model status endpoint, privacy documentation, dataset note, model card, curl examples and tests.

The API refuses prediction when the model has not been trained or loaded. This keeps the workflow explicit: generate data, train the model, then predict.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
requirements-optional-voice.txt  
.env.example  
.gitignore  
main.py  
ai_vocal_api_stipendio/dataset.py  
ai_vocal_api_stipendio/preprocessing.py  
ai_vocal_api_stipendio/model.py  
ai_vocal_api_stipendio/persistence.py  
ai_vocal_api_stipendio/service.py  
ai_vocal_api_stipendio/schemas.py  
ai_vocal_api_stipendio/api.py  
ai_vocal_api_stipendio/cli.py  
ai_vocal_api_stipendio/voice_assistant.py  
docs/dataset_note.md  
docs/model_card.md  
docs/privacy_note.md  
docs/api_usage.md  
docs/curl_examples.md  
docs/train_before_predict.md  
docs/portfolio_summary.md  
issues/001_train_before_predict.md  
issues/002_privacy_and_voice_layer.md  
issues/003_api_validation.md  
labels/repo_labels.md  
data/synthetic_salary_profiles.csv  
models/.gitkeep  
transcripts/demo_transcript.txt  
screenshots/.gitkeep  
tests/test_dataset_model_service.py  

## Quick start

Create a virtual environment if desired, install dependencies and generate the default synthetic dataset.

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py generate-data
python3 main.py train
python3 main.py predict --age 32 --experience 8 --education-level 3 --current-salary 52000

Run the API:

python3 main.py serve

Then open:

http://127.0.0.1:8000/docs

## API workflow

Generate dataset.

Train model.

Call prediction endpoint.

The prediction endpoint intentionally requires an available trained model. If no model exists, train first with the CLI or call the train endpoint.

## Optional voice helper

Optional voice dependencies are kept separate.

pip install -r requirements-optional-voice.txt

The voice helper can create a spoken answer file with gTTS, but that may use an external service. Do not use private data in voice tests.

## Portfolio value

This project demonstrates how a small ML model can be wrapped into a real API and CLI while preserving responsible documentation. It is stronger than a single notebook because it has structure, model persistence, API schemas, validation, docs and tests.
