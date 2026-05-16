from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Tetris Pygame reconstructed skeleton.")
    parser.add_argument("--seed", type=int, default=None, help="Reserved for future deterministic game launch.")
    args = parser.parse_args()

    from .pygame_app import run_app
    run_app()


if __name__ == "__main__":
    main()
