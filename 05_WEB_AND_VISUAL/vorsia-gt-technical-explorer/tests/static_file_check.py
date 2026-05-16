from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(relative: str) -> None:
    path = ROOT / relative
    assert path.exists(), f"missing required file: {relative}"


def main() -> None:
    required = [
        "index.html",
        "style.css",
        "src/data.js",
        "src/vehicle_canvas.js",
        "src/dashboard.js",
        "src/app.js",
        "README.md",
        "docs/concept_brief.md",
        "docs/accessibility_notes.md",
        "docs/known_limitations.md",
    ]

    for relative in required:
        require(relative)

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    concept = (ROOT / "docs" / "concept_brief.md").read_text(encoding="utf-8").lower()
    limitations = (ROOT / "docs" / "known_limitations.md").read_text(encoding="utf-8").lower()

    assert 'type="module"' in html
    assert "src/app.js" in html

    combined = readme + "\n" + concept + "\n" + limitations

    assert "fictional" in combined
    assert "not affiliated" in combined or "no manufacturer affiliation" in combined
    assert "not a real vehicle" in combined or "not as a real vehicle" in combined
    assert "portfolio" in combined

    print("[OK] Static file check passed.")


if __name__ == "__main__":
    main()
