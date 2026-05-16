# Tetris Pygame

This repository is a clean reconstructed skeleton of the old Tetris Pygame project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements a playable Tetris-style game with a shared pure Python core and a Pygame interface. The core can be tested without opening a graphical window. The Pygame layer handles rendering, keyboard input, timing, pause/reset and high score persistence.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Game type: Tetris-style falling block puzzle  
Main interface: Pygame  
Core engine: pure Python, testable without Pygame  
Music claim: none  
Portfolio readiness: prepared baseline  

## Features

The reconstructed baseline includes the seven classic tetrominoes, board collision, piece rotation, soft drop, hard drop, line clearing, score calculation, level progression, next-piece preview, hold-piece mechanic, pause, reset and persistent high score file.

The project includes a small Super Rotation System-inspired wall kick approximation. It is not a full official SRS implementation, but the documentation explains the current behavior and future direction.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
tetris_pygame/tetrominoes.py  
tetris_pygame/core.py  
tetris_pygame/highscore.py  
tetris_pygame/pygame_app.py  
tetris_pygame/launcher.py  
docs/game_design.md  
docs/srs_notes.md  
docs/controls_and_usage.md  
docs/highscore_note.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_rotation_and_wall_kicks.md  
issues/002_highscore_and_settings.md  
issues/003_screenshot_gallery.md  
labels/repo_labels.md  
assets/.gitkeep  
data/.gitkeep  
screenshots/.gitkeep  
tests/test_core.py  

## Quick start

Install dependencies and run:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

Run a core smoke test without Pygame:

PYTHONPATH=. python3 -m pytest tests

## Controls

Left and Right move the active piece.

Down performs soft drop.

Up or X rotates clockwise.

Z rotates counterclockwise.

Space performs hard drop.

C holds the current piece.

P pauses or resumes.

R resets the game.

Escape or Q exits.

## Educational purpose

This project is useful because Tetris is simple to understand but still forces good architecture. The board, piece state, collision detection and line clearing should not depend on rendering. The Pygame layer should only display state and translate player input.

## Portfolio value

The strongest portfolio angle is the separation between core logic and UI. The project shows game-loop design, state modeling, collision logic, deterministic tests, Pygame rendering and structured documentation.

## Responsible reconstruction note

This is a reconstructed educational Tetris-style project. It does not claim to be an official Tetris implementation or a clone of the original historical repository.
