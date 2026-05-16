# API usage

Start the server with:

python3 main.py serve

The API runs by default on:

http://127.0.0.1:8000

Interactive documentation is available at:

http://127.0.0.1:8000/docs

Important endpoints:

GET /health

GET /status

GET /dataset

POST /train

POST /predict

The prediction endpoint returns HTTP 409 if no trained model is available. Train first with the CLI or with POST /train.
