# Curl examples

Start the server:

python3 main.py serve

Health check:

curl http://127.0.0.1:8000/health

Status:

curl http://127.0.0.1:8000/status

Train model:

curl -X POST http://127.0.0.1:8000/train \
  -H "Content-Type: application/json" \
  -d '{"regenerate_dataset": false, "samples": 800, "seed": 42}'

Predict:

curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 32, "experience": 8, "education_level": 3, "current_salary": 52000}'
