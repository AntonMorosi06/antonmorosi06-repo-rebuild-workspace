from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Genetic Algorithm Optimizer Visualizer reconstructed skeleton.")
    parser.add_argument("--landscape", default="sphere", help="Reserved for future CLI landscape launch.")
    args = parser.parse_args()

    from .pygame_app import run_app
    run_app()


if __name__ == "__main__":
    main()
