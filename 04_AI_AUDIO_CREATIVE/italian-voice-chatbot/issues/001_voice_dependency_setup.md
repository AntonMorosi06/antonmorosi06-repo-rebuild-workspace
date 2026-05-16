# Issue 001 - Voice dependency setup

## Goal

Document and stabilize optional voice mode.

## Current implementation

Text mode works with lightweight dependencies. Voice mode requires SpeechRecognition, pyttsx3 and PyAudio.

## Open points

PyAudio installation can fail on some systems.

Microphone permission may need to be enabled manually.

Speech recognition backend behavior may vary.

Italian TTS voice quality depends on installed system voices.

## Acceptance criteria

README explains optional voice installation.

Voice errors are caught and explained.

Text mode remains available even if voice dependencies are missing.
