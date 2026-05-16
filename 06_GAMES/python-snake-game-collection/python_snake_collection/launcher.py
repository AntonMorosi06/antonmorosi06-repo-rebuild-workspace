from __future__ import annotations

import argparse


MODES = ["text", "curses", "tkinter", "pygame"]


def run_mode(mode: str) -> None:
    if mode == "text":
        from .snake_text import run_text_demo
        run_text_demo()
        return

    if mode == "curses":
        from .snake_curses import run_curses
        run_curses()
        return

    if mode == "tkinter":
        from .snake_tkinter import run_tkinter
        run_tkinter()
        return

    if mode == "pygame":
        from .snake_pygame import run_pygame
        run_pygame()
        return

    raise ValueError(f"unknown mode: {mode}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Python Snake Game Collection launcher.")
    parser.add_argument("--mode", choices=MODES, default="text", help="Game interface to launch.")
    parser.add_argument("--list-modes", action="store_true", help="List available modes and exit.")
    args = parser.parse_args()

    if args.list_modes:
        print("Available modes:")
        for mode in MODES:
            print("-", mode)
        return

    try:
        run_mode(args.mode)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
