# AI Music Composer

This repository is a clean reconstructed skeleton of the old AI music creator project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements a small generative music composer in Python. It creates melody, bass, chords, drums and pad-like harmonic layers using a simple Markov and n-gram inspired approach. It exports a standard MIDI file using a pure Python MIDI writer and can also export a simple WAV preview using only the Python standard library.

The purpose is educational and portfolio-oriented. The repository demonstrates procedural music generation, symbolic music representation, MIDI writing, simple synthesis, reproducible seeds, project packaging, documentation, tests and output reports.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Generation model: simple Markov and weighted n-gram style transitions  
MIDI export: pure Python standard MIDI writer  
WAV export: simple standard-library sine-wave preview  
External services: none  
Production music claim: none  
Portfolio readiness: prepared baseline  

## Features

The composer can generate a complete short piece with multiple layers.

Melody is generated from a scale-aware transition model.

Bass follows the harmonic root movement.

Chords are generated as triads or seventh-like voicings depending on style.

Drums are represented as MIDI percussion events.

Pad notes reinforce the harmonic background.

The MIDI writer is implemented locally so the project can run without installing heavy MIDI libraries.

The WAV preview is intentionally simple. It is not a professional synthesizer. It provides a quick audible check using basic sine waves.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
ai_music_composer/music_theory.py  
ai_music_composer/markov.py  
ai_music_composer/composer.py  
ai_music_composer/midi_writer.py  
ai_music_composer/wav_synth.py  
ai_music_composer/reporting.py  
ai_music_composer/cli.py  
docs/markov_model.md  
docs/midi_pipeline.md  
docs/wav_preview.md  
docs/controls_and_usage.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_markov_transition_quality.md  
issues/002_midi_and_wav_exports.md  
issues/003_example_gallery.md  
labels/repo_labels.md  
examples/style_presets.md  
outputs/midi/.gitkeep  
outputs/wav/.gitkeep  
outputs/reports/.gitkeep  
screenshots/.gitkeep  
tests/test_music_generation.py  

## Quick start

Create a virtual environment if desired, install the lightweight test dependency and generate a demo composition.

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py generate --style cinematic --seed 42 --name demo_cinematic

Generate another style:

python3 main.py generate --style ambient --seed 11 --name demo_ambient

Available styles in this baseline:

cinematic  
ambient  
arcade  
dark  

## Output

The command creates:

A MIDI file in outputs/midi.

A WAV preview in outputs/wav.

A Markdown report in outputs/reports.

The report stores generation parameters, tempo, key, scale, style, number of events and output paths.

## Educational purpose

This project explains how algorithmic composition can be structured without pretending that the model is a large neural music system. It uses deterministic rules, weighted transitions and small stochastic choices. This makes the generation understandable and debuggable.

The project can later be expanded with real training data, external MIDI parsing, richer harmony, better rhythm models, neural sequence models or a web player.

## Important limitation

This project does not claim to generate professional music. It is an educational algorithmic composition baseline.
