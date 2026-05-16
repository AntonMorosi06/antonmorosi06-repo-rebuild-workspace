from __future__ import annotations

import argparse
from pathlib import Path

from .chatbot import ChatBot
from .voice_io import VoiceDependencyError, VoiceIO


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTS_DIR = PROJECT_ROOT / "transcripts"


def print_header() -> None:
    print("")
    print("Italian Voice Chatbot - Reconstructed Skeleton")
    print("Modalità testo sempre disponibile. Modalità voce opzionale.")
    print("Scrivi /help per aiuto, /save per salvare, esci per chiudere.")
    print("")


def run_text_chat() -> None:
    bot = ChatBot()
    print_header()

    while True:
        try:
            user_text = input("Tu: ").strip()
        except EOFError:
            print("")
            break

        if not user_text:
            continue

        if user_text == "/save":
            path = bot.save_transcript(TRANSCRIPTS_DIR)
            print(f"[OK] Transcript salvato: {path}")
            continue

        response = bot.reply(user_text)
        print(f"Bot: {response}")

        if bot.should_exit(user_text):
            break

    path = bot.save_transcript(TRANSCRIPTS_DIR)
    print(f"[OK] Transcript finale salvato: {path}")


def run_voice_chat() -> None:
    bot = ChatBot()
    voice = VoiceIO()

    print_header()
    voice.speak("Ciao, sono il chatbot vocale italiano. Puoi parlare ora.")

    while True:
        try:
            user_text = voice.listen_once().strip()
        except VoiceDependencyError as exc:
            print(f"[VOICE ERROR] {exc}")
            print("[INFO] Ritorno consigliato: python3 main.py --mode text")
            break

        if not user_text:
            response = "Non ho capito bene. Puoi ripetere?"
            print(f"Bot: {response}")
            voice.speak(response)
            continue

        print(f"Tu: {user_text}")

        response = bot.reply(user_text)
        print(f"Bot: {response}")
        voice.speak(response)

        if bot.should_exit(user_text):
            break

    path = bot.save_transcript(TRANSCRIPTS_DIR)
    print(f"[OK] Transcript finale salvato: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Italian rule-based text and optional voice chatbot.")
    parser.add_argument(
        "--mode",
        choices=["text", "voice"],
        default="text",
        help="Run text mode or optional voice mode.",
    )
    args = parser.parse_args()

    if args.mode == "voice":
        run_voice_chat()
    else:
        run_text_chat()


if __name__ == "__main__":
    main()
