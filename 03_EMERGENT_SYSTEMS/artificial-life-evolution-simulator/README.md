# Artificial Life Evolution Simulator

This repository is a clean reconstructed skeleton of the old artificial life and genetic evolution simulator. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project simulates a small artificial ecosystem with prey creatures, predator creatures, food resources, energy, DNA traits, mutation, reproduction, day and night, seasons, environmental events, minimap visualization and population statistics. The purpose is not to create a biologically exact ecosystem, but to make evolutionary and emergent-system concepts visible through an interactive Pygame simulation.

The strongest idea behind this project is that behavior is not hardcoded as one fixed script. Each creature is generated from a DNA profile. DNA influences speed, vision, aggression, sociability, fertility, metabolism, nocturnality, longevity and color. When creatures reproduce, their DNA is inherited with mutation. Over time, the ecosystem can drift toward different behavioral tendencies depending on food availability, predator pressure and environmental events.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Simulation type: Pygame artificial life and evolutionary ecosystem  
Hardware validation: not applicable  
Biological claim: educational and conceptual only  
Portfolio readiness: prepared baseline  
Screenshots: supported through runtime command  

## Features

The simulation includes two creature types: prey and predators. Prey search for food, avoid predators, reproduce when energy is high and die when age or energy constraints become critical. Predators search for prey, gain energy by hunting and reproduce less frequently.

The DNA model includes behavioral traits such as aggression, sociability, fertility and nocturnality. These traits are simple numeric parameters, but they make the population more interesting than a purely random particle system.

The world includes day and night cycles, seasonal multipliers, food regeneration, environmental events, spatial hashing for nearby-neighbor queries, minimap visualization and a side dashboard with population statistics.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
artificial_life_evolution/config.py  
artificial_life_evolution/dna.py  
artificial_life_evolution/food.py  
artificial_life_evolution/creature.py  
artificial_life_evolution/spatial_hash.py  
artificial_life_evolution/world.py  
artificial_life_evolution/app.py  
docs/ecosystem_model.md  
docs/dna_model.md  
docs/controls_and_usage.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_spatial_hash_performance.md  
issues/002_population_balance.md  
issues/003_screenshot_gallery.md  
labels/repo_labels.md  
screenshots/.gitkeep  
data/.gitkeep  
tests/test_dna.py  

## Quick start

Create a virtual environment if desired, install the dependencies and run the simulator.

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

## Controls

Space pauses or resumes the simulation.  
R resets the ecosystem.  
F adds food at the mouse position.  
P adds a prey creature at the mouse position.  
X adds a predator creature at the mouse position.  
E triggers a random environmental event.  
M toggles the minimap.  
T toggles trails.  
H toggles the help overlay.  
S saves a screenshot into the screenshots folder.  
Escape exits the application.

## Educational purpose

This repository is meant to explain artificial life, emergent behavior and genetic evolution through a visible simulation. The user can observe how local rules produce global ecosystem patterns. No creature has a complete understanding of the world. Each creature only reacts to nearby food, nearby predators, nearby prey and its own energy state.

The project can also be connected conceptually to MicroBot and swarm simulation. A similar system could later be adapted to model distributed agents, local sensing, energy constraints, swarm density, survival-like objective functions and adaptive behavior in simulated environments.

## Notes

This repository is intentionally small enough to be readable, but rich enough to serve as a serious reconstructed baseline. It should be treated as a clean educational skeleton, not as a recovered full historical source tree.
