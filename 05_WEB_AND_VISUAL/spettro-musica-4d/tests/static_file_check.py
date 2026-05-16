from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist():
    required = [
        "index.html",
        "style.css",
        "src/audio_engine.js",
        "src/tesseract.js",
        "src/particle_field.js",
        "src/visual_lab.js",
        "src/app.js",
        "README.md",
    ]

    for relative in required:
        assert (ROOT / relative).exists(), relative


def test_index_references_module_script():
    html = (ROOT / "index.html").read_text(encoding="utf-8")

    assert 'type="module"' in html
    assert "src/app.js" in html


def test_conceptual_warning_present():
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()

    assert "does not prove" in readme
    assert "physical" in readme
