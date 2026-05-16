from __future__ import annotations

import argparse
from pathlib import Path

from .composer import available_styles, compose
from .midi_writer import write_midi
from .reporting import save_report
from .wav_synth import render_wav_preview


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MIDI_DIR = PROJECT_ROOT / "outputs" / "midi"
WAV_DIR = PROJECT_ROOT / "outputs" / "wav"
REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"


def safe_name(name: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in name.strip())
    return cleaned or "generated_piece"


def cmd_generate(args: argparse.Namespace) -> None:
    name = safe_name(args.name)
    composition = compose(style=args.style, seed=args.seed, title=name)

    midi_path = MIDI_DIR / f"{name}.mid"
    wav_path = WAV_DIR / f"{name}.wav"
    report_path = REPORT_DIR / f"{name}.runtime.md"

    write_midi(composition, midi_path)
    render_wav_preview(composition, wav_path)
    save_report(composition, midi_path, wav_path, report_path)

    print("[OK] Composition generated")
    print("[OK] Title:", composition.title)
    print("[OK] Style:", composition.style)
    print("[OK] Key:", f"{composition.key.root} {composition.key.scale}")
    print("[OK] Tempo:", composition.tempo)
    print("[OK] Events:", len(composition.events))
    print("[OK] MIDI:", midi_path)
    print("[OK] WAV:", wav_path)
    print("[OK] Report:", report_path)


def cmd_styles(args: argparse.Namespace) -> None:
    print("Available styles:")
    for style in available_styles():
        print("-", style)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Music Composer reconstructed skeleton.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate a MIDI and WAV preview.")
    generate_parser.add_argument("--style", choices=available_styles(), default="cinematic")
    generate_parser.add_argument("--seed", type=int, default=42)
    generate_parser.add_argument("--name", default="generated_piece")
    generate_parser.set_defaults(func=cmd_generate)

    styles_parser = subparsers.add_parser("styles", help="List available styles.")
    styles_parser.set_defaults(func=cmd_styles)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
