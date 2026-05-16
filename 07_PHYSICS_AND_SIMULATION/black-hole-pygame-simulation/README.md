# Black Hole Pygame Simulation

This repository is a clean reconstructed skeleton of the old Black Hole Simulation project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements a visual black-hole-inspired particle simulation using Python and Pygame. The simulation includes orbiting particles, an event horizon region, accretion disk behavior, absorption shockwaves, relativistic-looking visual trails, polar jets and runtime controls for spawn modes and rendering modes.

This project is educational and visual. It is not a numerically accurate general relativity solver. It uses simplified Newtonian-style attraction, visual heuristics and artistic rendering to explain concepts such as gravity wells, accretion, absorption, orbital motion and energy emission.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Project type: Pygame physics-inspired visualization  
Core engine: pure Python and testable without Pygame  
Physics claim: simplified educational model  
Rendering: Pygame runtime  
Portfolio readiness: prepared baseline  

## Features

The simulation contains a central black hole, particle spawning modes, gravitational acceleration, particle absorption, shockwave generation, trail rendering, polar jets, accretion disk coloring, pause/reset controls, fullscreen toggle and screenshot export.

The core simulation is separated from the Pygame interface. This allows the physical state update, particle absorption and spawning behavior to be tested without opening a window.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
black_hole_pygame/config.py  
black_hole_pygame/vector.py  
black_hole_pygame/entities.py  
black_hole_pygame/simulation.py  
black_hole_pygame/rendering.py  
black_hole_pygame/pygame_app.py  
black_hole_pygame/launcher.py  
docs/physics_model.md  
docs/visual_model.md  
docs/controls_and_usage.md  
docs/scientific_limitations.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_physics_parameter_tuning.md  
issues/002_visual_modes_and_screenshots.md  
issues/003_future_web_port.md  
labels/repo_labels.md  
assets/.gitkeep  
data/.gitkeep  
screenshots/.gitkeep  
tests/test_simulation_core.py  

## Quick start

Install dependencies and run:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

Run core tests without opening Pygame:

PYTHONPATH=. python3 -m pytest tests

## Controls

Space pauses or resumes the simulation.

R resets the simulation.

1 selects edge spawn mode.

2 selects disk spawn mode.

3 selects spiral spawn mode.

4 selects rain spawn mode.

5 selects cluster spawn mode.

T toggles trails.

J toggles jets.

D toggles debug overlay.

S saves a screenshot.

F toggles fullscreen.

Escape or Q exits.

## Educational purpose

The project demonstrates how a visual physics-inspired simulation can be structured cleanly. The simulation core owns particles, attraction, absorption and shockwaves. The Pygame layer owns rendering, controls and screenshots.

## Responsible scientific framing

This is not a real black hole physics simulator. It does not solve Einstein field equations, relativistic geodesics, ray tracing around curved spacetime or accurate accretion plasma dynamics. It is an educational and artistic simulation inspired by black-hole concepts.

## Portfolio value

The strongest portfolio angle is the combination of visual impact and clean architecture. The repository contains a testable core, a graphical runtime, documentation, limitations and a clear path for future upgrades.
