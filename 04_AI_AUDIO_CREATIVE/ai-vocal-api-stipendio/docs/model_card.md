# Model card

## Model name

AI Vocal API Stipendio reconstructed baseline.

## Model type

NumPy logistic regression classifier.

## Intended use

Educational demonstration of a trainable model served through CLI and FastAPI.

## Not intended use

The model must not be used for real salary prediction, hiring, compensation, finance, eligibility, educational, medical, legal or employment decisions.

## Input features

Age, experience, education_level and current_salary.

## Output

Binary synthetic class and probability.

## Data

Synthetic data generated locally by an artificial rule.

## Training procedure

The model standardizes the features, trains a logistic regression classifier and saves the scaler plus weights to a JSON file.

## Limitations

The model learns a synthetic pattern. Its accuracy says only how well it matches synthetic labels. It does not validate anything about real salary dynamics or real people.

## Safety note

The API responses include a warning that the result is educational only.
