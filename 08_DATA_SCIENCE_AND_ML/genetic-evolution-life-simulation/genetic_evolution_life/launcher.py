from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Genetic Evolution Life Simulation reconstructed skeleton.")
    parser.add_argument("--preset", default="balanced", help="Reserved for future CLI preset launch.")
    args = parser.parse_args()

    from .pygame_app import run_app
    run_app()


if __name__ == "__main__":
    main()
