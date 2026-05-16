# Issue 002 - MIDI and WAV exports

## Goal

Keep export formats stable and useful.

## Current implementation

The project exports MIDI through a pure Python writer and WAV through a simple standard-library renderer.

## Future improvements

Add optional MusicXML export.

Add optional external MIDI library support.

Add better instrument mapping.

Add stereo WAV rendering.

Add simple reverb or delay in WAV preview.

## Acceptance criteria

Core MIDI and WAV generation should remain dependency-light.
