from __future__ import annotations

from dataclasses import dataclass


NOTE_TO_SEMITONE = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}

SEMITONE_TO_NOTE = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B",
}

SCALE_PATTERNS = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "cinematic_minor": [0, 2, 3, 5, 7, 8, 11],
}


@dataclass(frozen=True)
class KeySignature:
    root: str
    scale: str

    @property
    def root_semitone(self) -> int:
        if self.root not in NOTE_TO_SEMITONE:
            raise ValueError(f"unknown root note: {self.root}")
        return NOTE_TO_SEMITONE[self.root]

    @property
    def scale_pattern(self) -> list[int]:
        if self.scale not in SCALE_PATTERNS:
            raise ValueError(f"unknown scale: {self.scale}")
        return SCALE_PATTERNS[self.scale]


def midi_note_name(note_number: int) -> str:
    semitone = note_number % 12
    octave = note_number // 12 - 1
    return f"{SEMITONE_TO_NOTE[semitone]}{octave}"


def scale_notes(key: KeySignature, octave: int = 4, octaves: int = 2) -> list[int]:
    base = (octave + 1) * 12 + key.root_semitone
    notes: list[int] = []

    for octave_index in range(octaves):
        for interval in key.scale_pattern:
            notes.append(base + octave_index * 12 + interval)

    return notes


def degree_to_note(key: KeySignature, degree: int, octave: int = 4) -> int:
    pattern = key.scale_pattern
    octave_offset = degree // len(pattern)
    degree_index = degree % len(pattern)
    return (octave + 1 + octave_offset) * 12 + key.root_semitone + pattern[degree_index]


def chord_from_degree(key: KeySignature, degree: int, octave: int = 3, seventh: bool = False) -> list[int]:
    root = degree_to_note(key, degree, octave)
    third = degree_to_note(key, degree + 2, octave)
    fifth = degree_to_note(key, degree + 4, octave)
    notes = [root, third, fifth]

    if seventh:
        notes.append(degree_to_note(key, degree + 6, octave))

    return notes


def clamp_midi(note: int) -> int:
    return max(0, min(127, int(note)))
