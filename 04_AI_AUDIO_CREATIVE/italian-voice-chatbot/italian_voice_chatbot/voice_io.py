from __future__ import annotations

from dataclasses import dataclass


class VoiceDependencyError(RuntimeError):
    pass


@dataclass
class VoiceIO:
    language: str = "it-IT"
    rate: int = 180

    def speak(self, text: str) -> None:
        try:
            import pyttsx3
        except Exception:
            print(f"[VOICE OUTPUT FALLBACK] {text}")
            return

        engine = pyttsx3.init()
        engine.setProperty("rate", self.rate)
        engine.say(text)
        engine.runAndWait()

    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 8) -> str:
        try:
            import speech_recognition as sr
        except Exception as exc:
            raise VoiceDependencyError(
                "SpeechRecognition is not installed. Install requirements-voice.txt or use --mode text."
            ) from exc

        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("[VOICE] Calibrazione rumore ambientale...")
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                print("[VOICE] Parla ora.")
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except Exception as exc:
            raise VoiceDependencyError(
                "Microphone access failed. Check permissions, input device and PyAudio installation."
            ) from exc

        try:
            return recognizer.recognize_google(audio, language=self.language)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:
            raise VoiceDependencyError(
                "Speech recognition backend request failed. Use text mode for offline-safe testing."
            ) from exc
