# Python Snake Game Collection

This repository is a clean reconstructed skeleton of the old Snake Game Collection project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project contains multiple Python implementations of the classic Snake game. The important design choice is that the game logic is shared in one core module, while each interface is kept separate. This makes the repository useful as a portfolio project because it demonstrates separation between game state, input handling, rendering and launch modes.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Game type: classic Snake  
Core engine: shared pure Python module  
Interfaces: text, curses, Tkinter and optional Pygame  
Portfolio readiness: prepared baseline  
Hardware validation: not applicable  

## Implementations

The collection currently includes four launch modes.

Text mode is a dependency-free simulation mode. It prints the board in the terminal and is useful for quick checks.

Curses mode is a terminal-based interactive Snake game for systems that support the curses module.

Tkinter mode is a desktop GUI Snake game using the Python standard library.

Pygame mode is an optional richer game window. It requires pygame to be installed separately.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
requirements-pygame.txt  
.gitignore  
main.py  
python_snake_collection/core.py  
python_snake_collection/launcher.py  
python_snake_collection/snake_text.py  
python_snake_collection/snake_curses.py  
python_snake_collection/snake_tkinter.py  
python_snake_collection/snake_pygame.py  
docs/game_design.md  
docs/controls_and_usage.md  
docs/pygame_optional_note.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_shared_core_engine.md  
issues/002_pygame_polish.md  
issues/003_screenshot_gallery.md  
labels/repo_labels.md  
assets/.gitkeep  
screenshots/.gitkeep  
tests/test_core.py  

## Quick start

Run text mode with no extra dependencies:

python3 main.py --mode text

Run Tkinter mode:

python3 main.py --mode tkinter

Run curses mode:

python3 main.py --mode curses

Run Pygame mode after installing the optional dependency:

pip install -r requirements-pygame.txt
python3 main.py --mode pygame

List modes:

python3 main.py --list-modes

## Controls

Arrow keys change direction in GUI modes.

WASD also works in Tkinter and Pygame modes.

Q quits in curses and Pygame modes.

R resets in Pygame mode.

Text mode runs a short deterministic demonstration.

## Educational purpose

This project shows how the same game logic can be reused across multiple interfaces. The shared core handles snake movement, food placement, score, collisions and reset. Renderers do not own the game rules. They only read the game state and translate user input into direction changes.

## Portfolio value

The strongest portfolio angle is architecture. Instead of having three disconnected Snake scripts, this reconstructed version uses a small shared engine and separate adapters. That makes the project easier to test, extend and explain.
