# Spettro Musica 4D

This repository is a clean reconstructed skeleton of the old Spettro-Musica-4D project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project is a static web lab for audio-reactive dimensional visualization. It combines Canvas rendering, Web Audio analysis, a rotating tesseract-inspired 4D projection, a spectrum field, an audio energy cube, conceptual dimensional controls and a placeholder area for a future GLB viewer.

The purpose is educational and visual. This project does not prove the physical existence of a fourth spatial dimension. It uses 4D as a mathematical and informational visualization model: points are represented in four coordinates, projected into 3D-like and 2D screen space, and modulated by audio energy.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Project type: static HTML/CSS/JS web lab  
Main technologies: Canvas, Web Audio API, modular JavaScript  
Microphone access: optional and user-triggered  
Physical claim: none  
Portfolio readiness: prepared baseline  
GitHub Pages readiness: prepared baseline  

## Features

The page includes a visual dashboard, an audio analyzer, a tesseract projection, particle spectrum, dimension sliders, audio cube, conceptual 4D explanation and privacy note.

The app can run without microphone input using an internal synthetic signal. If the user clicks Start microphone, the browser asks for permission and the Web Audio analyser starts reacting to real audio.

The code is modular. The main files are split into audio engine, math and tesseract projection, particle field, UI/runtime logic and utility helpers.

## Repository layout

README.md  
CHANGELOG.md  
index.html  
style.css  
src/audio_engine.js  
src/tesseract.js  
src/particle_field.js  
src/visual_lab.js  
src/app.js  
docs/conceptual_model.md  
docs/privacy_microphone_note.md  
docs/github_pages_checklist.md  
docs/browser_test_checklist.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_audio_permission_and_privacy.md  
issues/002_glb_viewer_future_integration.md  
issues/003_screenshot_gallery.md  
labels/repo_labels.md  
assets/models/.gitkeep  
assets/img/.gitkeep  
screenshots/.gitkeep  
tests/static_file_check.py  

## Quick start

Open index.html directly in a browser, or serve the folder locally:

python3 -m http.server 8080

Then open:

http://127.0.0.1:8080

For microphone input, the browser may require localhost or HTTPS.

## Controls

Start microphone asks for microphone permission and uses the Web Audio API.

Stop microphone disables the live audio stream.

Synthetic mode keeps the visuals moving without microphone access.

The W-depth slider changes the fourth-dimensional projection depth.

The rotation slider changes projection motion.

The sensitivity slider changes audio-reactive intensity.

The reset button restores the default visual parameters.

## Responsible framing

This project treats 4D as a mathematical, computational and visual abstraction. It does not claim to demonstrate real four-dimensional physics. It is suitable for portfolio presentation, creative coding, educational explanation and possible connection to MicroBot dimensional-engine visualizations.

## MicroBot connection

In the MicroBot ecosystem, this kind of page can become a visual module for dimensional state representation, telemetry fields, frequency-domain sensor response, gesture/audio interaction or simulation dashboards. The correct interpretation is informational visualization, not physical proof.
