# STT and TTS limitations

Speech-to-text and text-to-speech are system-dependent. On macOS, microphone permission, Python version, PyAudio installation, selected input device and installed system voices can all affect behavior.

For this reason, the repository treats voice as optional. The text mode is the stable default path.

Common issues include missing PyAudio, denied microphone permission, noisy input, unsupported microphone devices, speech recognition request errors and unavailable Italian text-to-speech voices.

If voice mode fails, use:

python3 main.py --mode text

This keeps the chatbot usable while audio dependencies are fixed separately.
