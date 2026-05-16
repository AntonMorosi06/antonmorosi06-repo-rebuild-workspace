# Genetic Evolution Life Simulation

This repository is a clean reconstructed skeleton of the old genetic evolution / artificial life simulation project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements an educational artificial-life simulation using Python and Pygame. Agents move inside a 2D world, consume food, spend energy, age, reproduce when they have enough energy and pass mutated genomes to offspring. Over time, the population can show selection pressure, adaptation, collapse, recovery, drift and emergent behavior.

The architecture separates the simulation core from the Pygame interface. The evolutionary logic, genome mutation, agent behavior, reproduction, death and metrics can be tested without opening a graphical window.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Project type: artificial life / evolutionary simulation  
Algorithmic theme: genetic inheritance, mutation and selection pressure  
Interface: Pygame  
Core engine: pure Python and testable without Pygame  
External ML dependency: none  
Portfolio readiness: prepared baseline  

## Features

The simulation includes a 2D world, agents, food, energy, age, movement, perception radius, metabolism, reproduction threshold, mutation, inherited traits, population metrics and runtime visualization.

Each agent has a genome with speed, perception, metabolism, size, fertility and mutation intensity. These traits affect survival and reproduction.

Food appears in the environment. Agents search for nearby food if they can perceive it; otherwise they wander. Eating increases energy. Movement and metabolism consume energy. Agents die if energy reaches zero or if they exceed maximum age.

When an agent has enough energy, it can reproduce. The offspring receives a mutated copy of the parent genome.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
genetic_evolution_life/vector.py  
genetic_evolution_life/genome.py  
genetic_evolution_life/entities.py  
genetic_evolution_life/world.py  
genetic_evolution_life/simulation.py  
genetic_evolution_life/metrics.py  
genetic_evolution_life/palette.py  
genetic_evolution_life/pygame_app.py  
genetic_evolution_life/launcher.py  
docs/artificial_life_model.md  
docs/evolution_model.md  
docs/controls_and_usage.md  
docs/metrics_explained.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_balance_population_dynamics.md  
issues/002_lineage_and_export.md  
issues/003_microbot_swarm_mapping.md  
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

N advances one simulation step when paused.

R resets the world.

F adds food.

A adds agents.

1 selects balanced ecosystem preset.

2 selects scarce food preset.

3 selects abundant food preset.

4 selects high mutation preset.

5 selects predator-free drift preset.

T toggles trails.

D toggles debug overlay.

S saves a screenshot.

Escape or Q exits.

## Educational purpose

This project is useful because it makes evolutionary concepts visible. The user can observe how traits interact with survival pressure. High speed may find food faster but may cost more energy. High perception may improve food seeking but can be expensive. High fertility may spread a lineage quickly but can collapse if food becomes scarce.

The simulation is not a biological proof. It is a simplified artificial-life model designed to explain inheritance, mutation, selection and population dynamics.

## Portfolio value

The strongest portfolio angle is the combination of evolutionary modeling and visual simulation. The repository demonstrates pure Python simulation architecture, agent behavior, genome mutation, metrics, Pygame rendering, documentation and tests.

## Responsible reconstruction note

This is a reconstructed educational artificial-life project. It should be presented as a clean baseline, not as a recovered full historical source tree.
