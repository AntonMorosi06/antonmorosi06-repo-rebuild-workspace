# Space Invaders Pygame

This repository is a clean reconstructed skeleton of the old Space Invaders style Pygame project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements a playable arcade shooter inspired by the classic Space Invaders formula. The architecture separates the pure Python game core from the Pygame rendering layer. This means movement, bullets, aliens, collision detection, scoring, waves and game-over logic can be tested without opening a graphical window.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Game type: arcade shooter  
Main interface: Pygame  
Core engine: pure Python, testable without Pygame  
External assets: none required  
Portfolio readiness: prepared baseline  

## Features

The reconstructed baseline includes a player ship, alien formation, player bullets, alien bullets, wave progression, horizontal invader movement, formation descent, collision detection, lives, score, level, pause, reset and local high score persistence.

The game uses generated shapes instead of external images. This keeps the repository lightweight and runnable immediately after installing Pygame.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
space_invaders_pygame/config.py  
space_invaders_pygame/core.py  
space_invaders_pygame/highscore.py  
space_invaders_pygame/pygame_app.py  
space_invaders_pygame/launcher.py  
docs/game_design.md  
docs/controls_and_usage.md  
docs/highscore_note.md  
docs/asset_strategy.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_core_gameplay_balance.md  
issues/002_assets_and_sound_future.md  
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

Run core tests without opening Pygame:

PYTHONPATH=. python3 -m pytest tests

## Controls

Left and Right move the player ship.

A and D also move the player ship.

Space fires.

P pauses or resumes.

R resets the game.

Escape or Q exits.

## Educational purpose

This project is useful because a classic arcade shooter has multiple interacting systems: player motion, enemy formation motion, bullets, collision detection, score state, difficulty progression and runtime rendering. Keeping those systems separated makes the code easier to test and explain.

## Portfolio value

The strongest portfolio angle is the architecture. The project is not just a single Pygame file. It contains a testable core, runtime adapter, high score helper, documentation and a clear path for future assets, sounds and menus.

## Responsible reconstruction note

This is a reconstructed educational arcade shooter inspired by a classic genre. It does not claim to be an official Space Invaders implementation or a recovered historical source tree.
