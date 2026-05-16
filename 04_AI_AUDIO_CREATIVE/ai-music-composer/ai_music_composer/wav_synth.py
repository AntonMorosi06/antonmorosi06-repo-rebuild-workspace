from __future__ import annotations

from pathlib import Path
import math
import struct
import wave

from .composer import Composition


SAMPLE_RATE = 22050


def midi_to_frequency(note: int) -> float:
    return 440.0 * (2.0 ** ((note - 69) / 12.0))


def render_wav_preview(composition: Composition, path: Path, max_seconds: float = 45.0) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    seconds_per_beat = 60.0 / composition.tempo
    duration_seconds = min(max_seconds, composition.duration_beats * seconds_per_beat + 1.0)
    total_samples = int(duration_seconds * SAMPLE_RATE)
    buffer = [0.0 for _ in range(total_samples)]

    melodic_events = [
        event for event in composition.events
        if event.track in {"melody", "bass", "chords", "pad"}
    ]

    for event in melodic_events:
        start_sample = int(event.start * seconds_per_beat * SAMPLE_RATE)
        end_sample = int((event.start + event.duration) * seconds_per_beat * SAMPLE_RATE)
        end_sample = min(end_sample, total_samples)

        if end_sample <= start_sample:
            continue

        frequency = midi_to_frequency(event.note)
        amplitude = (event.velocity / 127.0) * 0.055

        if event.track == "bass":
            amplitude *= 1.25
        elif event.track == "pad":
            amplitude *= 0.55
        elif event.track == "chords":
            amplitude *= 0.65

        length = end_sample - start_sample
        attack = max(1, int(0.015 * SAMPLE_RATE))
        release = max(1, int(0.055 * SAMPLE_RATE))

        for index in range(length):
            sample_index = start_sample + index
            if sample_index >= total_samples:
                break

            t = sample_index / SAMPLE_RATE
            envelope = 1.0

            if index < attack:
                envelope = index / attack
            elif length - index < release:
                envelope = max(0.0, (length - index) / release)

            wave_value = math.sin(2.0 * math.pi * frequency * t)
            buffer[sample_index] += wave_value * amplitude * envelope

    for event in [event for event in composition.events if event.track == "drums"]:
        start_sample = int(event.start * seconds_per_beat * SAMPLE_RATE)
        length = int(0.08 * SAMPLE_RATE)
        amplitude = (event.velocity / 127.0) * 0.09

        for index in range(length):
            sample_index = start_sample + index
            if sample_index >= total_samples:
                break
            decay = 1.0 - (index / max(1, length))
            noise = math.sin(index * 0.83) * math.sin(index * 0.31)
            buffer[sample_index] += noise * amplitude * decay

    peak = max(0.01, max(abs(value) for value in buffer))
    scale = 0.86 / peak

    with wave.open(str(path), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        frames = bytearray()
        for value in buffer:
            sample = int(max(-1.0, min(1.0, value * scale)) * 32767)
            frames.extend(struct.pack("<h", sample))

        wav.writeframes(bytes(frames))

    return path
