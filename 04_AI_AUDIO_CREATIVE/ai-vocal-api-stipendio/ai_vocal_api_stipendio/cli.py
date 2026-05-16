from __future__ import annotations

import argparse
from pathlib import Path

from .service import SalaryPredictionService
from .voice_assistant import prediction_to_italian_text, save_tts_mp3


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_PATH = PROJECT_ROOT / "data" / "synthetic_salary_profiles.csv"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "salary_classifier.json"


def build_service() -> SalaryPredictionService:
    return SalaryPredictionService(
        dataset_path=DEFAULT_DATASET_PATH,
        model_path=DEFAULT_MODEL_PATH,
    )


def cmd_generate_data(args: argparse.Namespace) -> None:
    service = build_service()
    dataset = service.regenerate_dataset(samples=args.samples, seed=args.seed)
    print("[OK] Dataset generated:", DEFAULT_DATASET_PATH)
    print("[OK] Rows:", dataset.size)
    print("[OK] Positive rate:", round(dataset.positive_rate, 4))


def cmd_train(args: argparse.Namespace) -> None:
    service = build_service()
    result = service.train()
    print("[OK] Model trained")
    print("[OK] Backend:", result.backend)
    print("[OK] Accuracy:", round(result.accuracy, 4))
    print("[OK] Loss:", round(result.loss, 5))
    print("[OK] Dataset size:", result.dataset_size)
    print("[OK] Model path:", result.model_path)


def cmd_status(args: argparse.Namespace) -> None:
    service = build_service()
    status = service.status()
    for key, value in status.items():
        print(f"{key}: {value}")


def cmd_predict(args: argparse.Namespace) -> None:
    service = build_service()
    prediction = service.predict(
        age=args.age,
        experience=args.experience,
        education_level=args.education_level,
        current_salary=args.current_salary,
    )

    print("[OK] Prediction")
    print("label:", prediction["label"])
    print("class_name:", prediction["class_name"])
    print("probability:", round(float(prediction["probability"]), 4))
    print("warnings:", prediction["warnings"])
    print("model_warning:", prediction["model_warning"])

    if args.tts:
        text = prediction_to_italian_text(prediction)
        output = PROJECT_ROOT / "transcripts" / "last_prediction_voice.mp3"
        path = save_tts_mp3(text, output)
        print("[OK] TTS saved:", path)


def cmd_serve(args: argparse.Namespace) -> None:
    try:
        import uvicorn
        from .api import app
    except ModuleNotFoundError as exc:
        missing_name = getattr(exc, "name", "unknown")
        raise SystemExit(
            "[ERROR] Missing API dependency: "
            f"{missing_name}. Install API dependencies with: pip install -r requirements.txt"
        ) from exc

    uvicorn.run(app, host=args.host, port=args.port)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Vocal API Stipendio reconstructed skeleton.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate-data", help="Generate synthetic salary dataset.")
    generate_parser.add_argument("--samples", type=int, default=800)
    generate_parser.add_argument("--seed", type=int, default=42)
    generate_parser.set_defaults(func=cmd_generate_data)

    train_parser = subparsers.add_parser("train", help="Train and save the model.")
    train_parser.set_defaults(func=cmd_train)

    status_parser = subparsers.add_parser("status", help="Show dataset and model status.")
    status_parser.set_defaults(func=cmd_status)

    predict_parser = subparsers.add_parser("predict", help="Run one prediction.")
    predict_parser.add_argument("--age", type=float, required=True)
    predict_parser.add_argument("--experience", type=float, required=True)
    predict_parser.add_argument("--education-level", type=float, required=True)
    predict_parser.add_argument("--current-salary", type=float, required=True)
    predict_parser.add_argument("--tts", action="store_true", help="Save optional Italian TTS mp3.")
    predict_parser.set_defaults(func=cmd_predict)

    serve_parser = subparsers.add_parser("serve", help="Run FastAPI server.")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.set_defaults(func=cmd_serve)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
