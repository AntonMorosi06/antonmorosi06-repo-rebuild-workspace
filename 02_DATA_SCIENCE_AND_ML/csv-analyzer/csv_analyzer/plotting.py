from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def save_histograms(df, output_dir: str | Path) -> list[Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    numeric_df = df.select_dtypes(include="number")
    saved = []

    for column in numeric_df.columns:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(numeric_df[column].dropna(), bins=20)
        ax.set_title(f"Histogram: {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        fig.tight_layout()

        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in column)
        path = output_path / f"histogram_{safe_name}.png"
        fig.savefig(path)
        plt.close(fig)
        saved.append(path)

    return saved
