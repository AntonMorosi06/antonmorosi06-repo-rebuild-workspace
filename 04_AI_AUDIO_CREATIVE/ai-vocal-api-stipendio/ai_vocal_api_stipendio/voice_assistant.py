from __future__ import annotations

from pathlib import Path


def prediction_to_italian_text(prediction: dict[str, object]) -> str:
    probability = float(prediction["probability"])
    class_name = str(prediction["class_name"])
    warnings = prediction.get("warnings", [])

    text = (
        f"Risultato educativo: {class_name}. "
        f"Confidenza stimata: {probability:.3f}. "
        "Attenzione: questo modello usa dati sintetici e non deve essere usato per decisioni reali."
    )

    if warnings:
        text += " Sono presenti avvisi sui valori inseriti: " + "; ".join(str(item) for item in warnings)

    return text


def save_tts_mp3(text: str, output_path: Path, language: str = "it") -> Path:
    try:
        from gtts import gTTS
    except Exception as exc:
        raise RuntimeError("gTTS is not installed. Install requirements-optional-voice.txt to use TTS.") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tts = gTTS(text=text, lang=language)
    tts.save(str(output_path))
    return output_path
