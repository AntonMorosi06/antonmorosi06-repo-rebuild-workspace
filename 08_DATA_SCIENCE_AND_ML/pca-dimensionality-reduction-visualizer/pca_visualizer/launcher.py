from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="PCA Dimensionality Reduction Visualizer reconstructed skeleton.")
    parser.add_argument("--dataset", default="correlated", help="Reserved for future CLI dataset launch.")
    args = parser.parse_args()

    from .pygame_app import run_app
    run_app()


if __name__ == "__main__":
    main()
