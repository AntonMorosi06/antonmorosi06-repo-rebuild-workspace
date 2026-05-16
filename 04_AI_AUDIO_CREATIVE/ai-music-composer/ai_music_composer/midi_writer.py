from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import struct

from .composer import Composition, NoteEvent


TICKS_PER_BEAT = 480


def variable_length_quantity(value: int) -> bytes:
    if value < 0:
        raise ValueError("delta time cannot be negative")

    buffer = value & 0x7F
    value >>= 7

    bytes_out = []
    while value:
        bytes_out.insert(0, (buffer | 0x80))
        buffer = value & 0x7F
        value >>= 7

    bytes_out.append(buffer)
    return bytes(bytes_out)


def meta_event(delta: int, event_type: int, data: bytes) -> bytes:
    return variable_length_quantity(delta) + bytes([0xFF, event_type, len(data)]) + data


def midi_event(delta: int, status: int, data1: int, data2: int) -> bytes:
    return variable_length_quantity(delta) + bytes([status, data1 & 0x7F, data2 & 0x7F])


def tempo_meta_event(bpm: int) -> bytes:
    microseconds_per_quarter = int(60_000_000 / bpm)
    data = microseconds_per_quarter.to_bytes(3, byteorder="big")
    return meta_event(0, 0x51, data)


def track_name_event(name: str) -> bytes:
    encoded = name.encode("utf-8")
    return meta_event(0, 0x03, encoded)


def end_of_track_event(delta: int = 0) -> bytes:
    return variable_length_quantity(delta) + b"\xFF\x2F\x00"


def program_change(delta: int, channel: int, program: int) -> bytes:
    return variable_length_quantity(delta) + bytes([0xC0 | (channel & 0x0F), program & 0x7F])


def event_to_absolute_ticks(event: NoteEvent) -> tuple[int, int]:
    start = int(round(event.start * TICKS_PER_BEAT))
    end = int(round((event.start + event.duration) * TICKS_PER_BEAT))
    return start, max(start + 1, end)


def build_track(name: str, events: list[NoteEvent], tempo: int | None = None, program: int | None = None) -> bytes:
    raw = bytearray()
    raw.extend(track_name_event(name))

    if tempo is not None:
        raw.extend(tempo_meta_event(tempo))

    channel = events[0].channel if events else 0

    if program is not None and channel != 9:
        raw.extend(program_change(0, channel, program))

    timeline = []

    for event in events:
        start, end = event_to_absolute_ticks(event)
        timeline.append((start, 0, event))
        timeline.append((end, 1, event))

    timeline.sort(key=lambda item: (item[0], item[1]))

    previous_tick = 0
    for tick, event_kind, event in timeline:
        delta = tick - previous_tick
        previous_tick = tick

        if event_kind == 0:
            status = 0x90 | (event.channel & 0x0F)
            raw.extend(midi_event(delta, status, event.note, event.velocity))
        else:
            status = 0x80 | (event.channel & 0x0F)
            raw.extend(midi_event(delta, status, event.note, 0))

    raw.extend(end_of_track_event(0))
    return b"MTrk" + struct.pack(">I", len(raw)) + bytes(raw)


def write_midi(composition: Composition, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    tracks_by_name: dict[str, list[NoteEvent]] = defaultdict(list)
    for event in composition.events:
        tracks_by_name[event.track].append(event)

    track_order = ["melody", "bass", "chords", "pad", "drums"]
    program_map = {
        "melody": 81,
        "bass": 38,
        "chords": 89,
        "pad": 91,
        "drums": None,
    }

    tracks = []
    first = True
    for track_name in track_order:
        events = tracks_by_name.get(track_name, [])
        if not events:
            continue

        tracks.append(
            build_track(
                name=track_name,
                events=events,
                tempo=composition.tempo if first else None,
                program=program_map.get(track_name),
            )
        )
        first = False

    if not tracks:
        tracks.append(build_track("empty", [], tempo=composition.tempo))

    header = b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks), TICKS_PER_BEAT)
    path.write_bytes(header + b"".join(tracks))
    return path
