# Italian Voice Chatbot

This repository is a clean reconstructed skeleton of the old Italian voice chatbot project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements a small Italian rule-based chatbot with two operating modes. The first mode is a text-only command-line chat that always works with the lightweight dependencies. The second mode is an optional voice mode using SpeechRecognition for speech-to-text and pyttsx3 for text-to-speech when those packages and the local microphone setup are available.

The repository is intentionally structured as an educational baseline. It shows how to separate chatbot intent logic, normalization, response generation, optional voice input/output, transcript export, documentation and privacy notes.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Main language: Italian  
Main interface: command-line chat  
Voice input: optional  
Voice output: optional  
Cloud requirement: none by default  
Production claim: none  
Portfolio readiness: prepared baseline  

## Features

The chatbot supports greeting, identity, project explanation, MicroBot-related discussion, study support, motivation, help, privacy, time, goodbye and fallback responses.

The text chat mode is the default because it does not require a microphone, audio drivers or external speech packages.

The voice mode is optional because SpeechRecognition, microphone access and text-to-speech engines can behave differently depending on macOS, Python environment, drivers and installed system voices.

The project includes transcript logging. A transcript is saved into the transcripts directory at the end of a conversation. This is useful for debugging, portfolio demonstration and later improvement of the rule set.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
requirements-voice.txt  
.gitignore  
main.py  
italian_voice_chatbot/text_utils.py  
italian_voice_chatbot/intents.py  
italian_voice_chatbot/chatbot.py  
italian_voice_chatbot/voice_io.py  
italian_voice_chatbot/app.py  
docs/privacy_note.md  
docs/stt_tts_limitations.md  
docs/controls_and_usage.md  
docs/conversation_design.md  
docs/portfolio_summary.md  
issues/001_voice_dependency_setup.md  
issues/002_intent_expansion.md  
issues/003_transcript_examples.md  
labels/repo_labels.md  
transcripts/demo_transcript.txt  
screenshots/.gitkeep  
tests/test_chatbot.py  

## Quick start

Create a virtual environment if desired, install the lightweight dependencies and run the text chatbot.

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

Run explicit text mode:

python3 main.py --mode text

Optional voice support:

pip install -r requirements-voice.txt
python3 main.py --mode voice

## Commands

In text mode, write a message and press Enter.

Use exit, esci, quit or ciao to close the chat.

Use /help to show a short help message.

Use /save to save the current transcript manually.

## Educational purpose

This repository is meant to show how a small voice/chat assistant can be structured without pretending to be a large AI model. The assistant is rule-based and deterministic. It is useful for learning text normalization, intent matching, response design, optional speech input/output and privacy-aware transcript handling.

## Privacy note

The default text mode does not use a microphone. The optional voice mode uses local microphone input through the installed SpeechRecognition stack. This reconstructed baseline does not intentionally send conversations to a custom server. Some speech-recognition backends may use external services depending on configuration, so the user should read the documentation and avoid speaking private information during tests.
