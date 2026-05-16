# AI GUI Keras Classifier

This repository is a clean reconstructed skeleton of the old AI GUI work project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project demonstrates a small graphical machine learning application built around a synthetic classification problem. The app uses age, salary and experience as input features and predicts whether a synthetic profile belongs to a positive target class. The original project idea was a Tkinter GUI connected to a Keras classifier. This reconstructed version keeps that identity, but also includes a lightweight NumPy fallback classifier so that the repository remains runnable even when TensorFlow is not installed.

The repository is intended as a portfolio and learning baseline. It shows GUI design, dataset generation, feature scaling, model training, prediction, validation checks, documentation, model-card thinking and responsible limitations.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Main interface: Tkinter GUI  
Primary model path: optional Keras classifier  
Fallback model path: built-in NumPy logistic classifier  
Dataset type: synthetic educational dataset  
Production claim: none  
Portfolio readiness: prepared baseline  

## Why this structure

TensorFlow and Keras are powerful but heavy dependencies. On some machines, especially during quick rebuild workflows, forcing TensorFlow installation can slow the whole repository process. For this reason, this reconstructed baseline is designed in two layers.

If TensorFlow is installed, the app can train a small Keras neural network.

If TensorFlow is not installed, the app automatically uses a NumPy logistic classifier. This keeps the GUI and educational workflow usable while preserving the Keras direction of the original project.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
requirements-optional-keras.txt  
.gitignore  
main.py  
ai_gui_keras_classifier/dataset.py  
ai_gui_keras_classifier/preprocessing.py  
ai_gui_keras_classifier/numpy_classifier.py  
ai_gui_keras_classifier/keras_model.py  
ai_gui_keras_classifier/runtime.py  
ai_gui_keras_classifier/gui_app.py  
docs/dataset_note.md  
docs/model_card.md  
docs/ethics_and_limitations.md  
docs/controls_and_usage.md  
docs/portfolio_summary.md  
issues/001_tensorflow_optional_dependency.md  
issues/002_gui_validation_and_errors.md  
issues/003_screenshot_gallery.md  
labels/repo_labels.md  
data/synthetic_profiles.csv  
models/.gitkeep  
screenshots/.gitkeep  
tests/test_dataset_and_numpy_model.py  

## Quick start

Create a virtual environment if desired, install the lightweight dependencies and run the app.

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

Optional Keras support can be installed separately.

pip install -r requirements-optional-keras.txt

## GUI behavior

The GUI lets the user generate a synthetic dataset, train a classifier, enter age, salary and experience, and run a prediction. The app displays the predicted class, confidence score, selected backend and training metrics.

The GUI performs basic input validation. Age, salary and experience must be numeric. Values outside the documented educational range are accepted but flagged in the output message as extrapolation.

## Educational purpose

This project is designed to explain how a simple ML application is structured end to end. It includes synthetic data generation, feature scaling, model training, model prediction and a GUI layer. It also includes a model card and limitations document, because even toy machine learning projects should clearly describe what the data means and what the model should not be used for.

## Important limitation

This project uses synthetic data. It must not be used for real hiring, salary decisions, financial decisions, eligibility decisions or any serious evaluation of real people. The labels are generated from an artificial rule with added noise. The model only learns that artificial rule.
