from __future__ import annotations

from dataclasses import dataclass, field
import random

from .markov import MarkovMelodyModel, rhythm_pattern, velocity_pattern
from .music_theory import KeySignature, chord_from_degree, degree_to_note


@dataclass
class NoteEvent:
    track: str
    note: int
    start: float
    duration: float
    velocity: int
    channel: int = 0

    @property
    def end(self) -> float:
        return self.start + self.duration


@dataclass
class Composition:
    title: str
    style: str
    key: KeySignature
    tempo: int
    bars: int
    events: list[NoteEvent] = field(default_factory=list)

    @property
    def duration_beats(self) -> float:
        if not self.events:
            return 0.0
        return max(event.end for event in self.events)

    def track_names(self) -> list[str]:
        return sorted(set(event.track for event in self.events))


STYLE_PRESETS = {
    "cinematic": {
        "root": "D",
        "scale": "cinematic_minor",
        "tempo": 92,
        "bars": 12,
        "melody_octave": 5,
        "bass_octave": 2,
        "seventh": True,
    },
    "ambient": {
        "root": "A",
        "scale": "minor",
        "tempo": 72,
        "bars": 10,
        "melody_octave": 5,
        "bass_octave": 2,
        "seventh": True,
    },
    "arcade": {
        "root": "C",
        "scale": "pentatonic_minor",
        "tempo": 132,
        "bars": 8,
        "melody_octave": 5,
        "bass_octave": 3,
        "seventh": False,
    },
    "dark": {
        "root": "F#",
        "scale": "phrygian",
        "tempo": 84,
        "bars": 12,
        "melody_octave": 4,
        "bass_octave": 2,
        "seventh": True,
    },
}


def available_styles() -> list[str]:
    return sorted(STYLE_PRESETS.keys())


def harmonic_progression(style: str, bars: int) -> list[int]:
    if style == "ambient":
        pattern = [0, 5, 3, 4]
    elif style == "arcade":
        pattern = [0, 2, 4, 2]
    elif style == "dark":
        pattern = [0, 1, 5, 0]
    else:
        pattern = [0, 5, 2, 6]

    result = []
    for index in range(bars):
        result.append(pattern[index % len(pattern)])
    return result


def compose(style: str = "cinematic", seed: int = 42, title: str = "generated_piece") -> Composition:
    if style not in STYLE_PRESETS:
        raise ValueError(f"unknown style: {style}. Available styles: {', '.join(available_styles())}")

    preset = STYLE_PRESETS[style]
    rng = random.Random(seed)

    key = KeySignature(root=str(preset["root"]), scale=str(preset["scale"]))
    tempo = int(preset["tempo"])
    bars = int(preset["bars"])
    beats_per_bar = 4
    total_beats = bars * beats_per_bar

    composition = Composition(
        title=title,
        style=style,
        key=key,
        tempo=tempo,
        bars=bars,
    )

    progression = harmonic_progression(style, bars)
    melody_model = MarkovMelodyModel(scale_degrees=list(range(0, 7)))

    melody_steps = max(16, bars * 4)
    melody_degrees = melody_model.generate(length=melody_steps, rng=rng, start_degree=0)
    durations = rhythm_pattern(style, rng, melody_steps)
    velocities = velocity_pattern(style, rng, melody_steps)

    current = 0.0
    for degree, duration, velocity in zip(melody_degrees, durations, velocities):
        if current >= total_beats:
            break
        note = degree_to_note(key, degree, octave=int(preset["melody_octave"]))
        composition.events.append(
            NoteEvent(
                track="melody",
                note=note,
                start=current,
                duration=min(duration, total_beats - current),
                velocity=velocity,
                channel=0,
            )
        )
        current += duration

    for bar, root_degree in enumerate(progression):
        start = bar * beats_per_bar
        bass_note = degree_to_note(key, root_degree, octave=int(preset["bass_octave"]))
        composition.events.append(
            NoteEvent(
                track="bass",
                note=bass_note,
                start=start,
                duration=beats_per_bar * 0.92,
                velocity=82 if style != "ambient" else 62,
                channel=1,
            )
        )

        chord = chord_from_degree(
            key,
            root_degree,
            octave=3,
            seventh=bool(preset["seventh"]),
        )

        for chord_note in chord:
            composition.events.append(
                NoteEvent(
                    track="chords",
                    note=chord_note,
                    start=start,
                    duration=beats_per_bar * 0.86,
                    velocity=58 if style == "ambient" else 70,
                    channel=2,
                )
            )

        pad_shift = 12 if style in {"ambient", "cinematic"} else 0
        for pad_note in chord[:3]:
            composition.events.append(
                NoteEvent(
                    track="pad",
                    note=pad_note + pad_shift,
                    start=start,
                    duration=beats_per_bar * 1.00,
                    velocity=42 if style == "ambient" else 48,
                    channel=3,
                )
            )

    add_drums(composition, style=style, bars=bars)

    composition.events.sort(key=lambda event: (event.start, event.track, event.note))
    return composition


def add_drums(composition: Composition, style: str, bars: int) -> None:
    beats_per_bar = 4

    kick = 36
    snare = 38
    closed_hat = 42
    low_tom = 45

    for bar in range(bars):
        base = bar * beats_per_bar

        if style == "ambient":
            if bar % 2 == 0:
                composition.events.append(NoteEvent("drums", kick, base, 0.15, 52, channel=9))
            composition.events.append(NoteEvent("drums", closed_hat, base + 2.0, 0.10, 34, channel=9))

        elif style == "arcade":
            for offset in [0.0, 1.0, 2.0, 3.0]:
                composition.events.append(NoteEvent("drums", closed_hat, base + offset, 0.10, 72, channel=9))
            composition.events.append(NoteEvent("drums", kick, base + 0.0, 0.15, 96, channel=9))
            composition.events.append(NoteEvent("drums", snare, base + 2.0, 0.15, 92, channel=9))

        elif style == "dark":
            composition.events.append(NoteEvent("drums", kick, base + 0.0, 0.18, 88, channel=9))
            composition.events.append(NoteEvent("drums", low_tom, base + 2.5, 0.18, 68, channel=9))
            composition.events.append(NoteEvent("drums", closed_hat, base + 3.5, 0.08, 45, channel=9))

        else:
            composition.events.append(NoteEvent("drums", kick, base + 0.0, 0.16, 90, channel=9))
            composition.events.append(NoteEvent("drums", snare, base + 2.0, 0.16, 78, channel=9))
            composition.events.append(NoteEvent("drums", closed_hat, base + 1.0, 0.10, 50, channel=9))
            composition.events.append(NoteEvent("drums", closed_hat, base + 3.0, 0.10, 50, channel=9))
