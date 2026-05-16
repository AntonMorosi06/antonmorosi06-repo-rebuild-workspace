# Issue 002 - Privacy and voice layer

## Goal

Keep optional TTS functionality separate and privacy-aware.

## Current implementation

gTTS is optional and kept in requirements-optional-voice.txt. The project warns that TTS may contact an external service.

## Acceptance criteria

Core API must work without TTS packages.

No private data should be required for demos.

README and privacy note should explain the risk.
