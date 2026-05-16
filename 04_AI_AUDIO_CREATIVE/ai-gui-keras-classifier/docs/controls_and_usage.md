# Controls and usage

Run the app with:

python3 main.py

The GUI contains three input fields: age, salary and experience.

Use Train model to train the classifier. If TensorFlow is installed and the Keras preference is enabled, the app trains the Keras backend. Otherwise it trains the NumPy fallback classifier.

Use Predict to classify the current input profile.

Use Regenerate synthetic dataset to rebuild the local CSV file with deterministic synthetic data and reset the model.

The app displays backend, accuracy, loss, dataset size, positive rate, prediction label and confidence.
