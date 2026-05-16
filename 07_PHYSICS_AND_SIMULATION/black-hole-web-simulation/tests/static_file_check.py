from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(relative: str) -> None:
    path = ROOT / relative
    assert path.exists(), f"missing required file: {relative}"


def main() -> None:
    required = [
        "index.html",
        "style.css",
        "src/vector.js",
        "src/particle.js",
        "src/simulation.js",
        "src/renderer.js",
        "src/ui.js",
        "src/app.js",
        "README.md",
        "docs/scientific_limitations.md",
    ]

    for relative in required:
        require(relative)

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    limitations = (ROOT / "docs" / "scientific_limitations.md").read_text(encoding="utf-8").lower()

    assert 'type="module"' in html
    assert "src/app.js" in html
    assert "not a real general relativity simulator" in readme
    assert "does not solve einstein field equations" in limitations
    assert "canvas" in readme

    print("[OK] Static file check passed.")


if __name__ == "__main__":
    main()
