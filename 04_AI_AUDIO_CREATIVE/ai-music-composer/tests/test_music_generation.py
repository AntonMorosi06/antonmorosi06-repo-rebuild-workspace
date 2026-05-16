from pathlib import Path
import tempfile

from ai_music_composer.composer import available_styles, compose
from ai_music_composer.midi_writer import write_midi
from ai_music_composer.music_theory import KeySignature, scale_notes
from ai_music_composer.wav_synth import render_wav_preview


def test_available_styles_contains_expected_values():
    styles = available_styles()

    assert "cinematic" in styles
    assert "ambient" in styles
    assert "arcade" in styles
    assert "dark" in styles


def test_scale_notes_generates_midi_numbers():
    key = KeySignature(root="C", scale="major")
    notes = scale_notes(key, octave=4, octaves=1)

    assert notes[0] == 60
    assert len(notes) == 7


def test_compose_generates_events():
    composition = compose(style="cinematic", seed=42, title="test_piece")

    assert composition.events
    assert "melody" in composition.track_names()
    assert "bass" in composition.track_names()
    assert "drums" in composition.track_names()


def test_midi_writer_creates_file():
    composition = compose(style="ambient", seed=3, title="test_midi")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test.mid"
        write_midi(composition, path)

        assert path.exists()
        assert path.stat().st_size > 20


def test_wav_preview_creates_file():
    composition = compose(style="arcade", seed=4, title="test_wav")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test.wav"
        render_wav_preview(composition, path, max_seconds=3.0)

        assert path.exists()
        assert path.stat().st_size > 100
