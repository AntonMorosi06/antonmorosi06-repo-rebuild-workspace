# Genetic Algorithm Optimizer Visualizer

This repository is a clean reconstructed skeleton of the old genetic algorithm simulation project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements an educational genetic algorithm optimizer using Python and Pygame. The algorithm is implemented directly in the repository: real-valued genome representation, population initialization, fitness evaluation, tournament selection, blend crossover, Gaussian mutation, elitism, generation stepping and runtime metrics.

The architecture separates the genetic algorithm core from the Pygame interface. The optimizer, fitness landscapes and metrics can be tested without opening a graphical window.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Project type: evolutionary computation / machine learning visualization  
Algorithm: genetic algorithm implemented from scratch  
Interface: Pygame  
Core engine: pure Python and testable without Pygame  
External ML dependency: none  
Portfolio readiness: prepared baseline  

## Features

The visualizer includes multiple optimization landscapes: sphere, Rastrigin, Himmelblau, ridge and multi-peak.

Each individual is a two-dimensional real-valued genome represented as a point on the landscape.

The Pygame interface shows the fitness field, current population, elite individual, generation metrics, diversity, best fitness history and runtime parameters.

The user can switch landscapes, pause evolution, step one generation, reset population, change mutation rate, change crossover rate, change elite count, toggle trails and save screenshots.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
genetic_algorithm_visualizer/genome.py  
genetic_algorithm_visualizer/landscapes.py  
genetic_algorithm_visualizer/ga.py  
genetic_algorithm_visualizer/metrics.py  
genetic_algorithm_visualizer/palette.py  
genetic_algorithm_visualizer/pygame_app.py  
genetic_algorithm_visualizer/launcher.py  
docs/genetic_algorithm_theory.md  
docs/algorithm_walkthrough.md  
docs/controls_and_usage.md  
docs/landscape_notes.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_selection_and_mutation_tuning.md  
issues/002_step_by_step_visualization.md  
issues/003_export_history_and_gallery.md  
labels/repo_labels.md  
assets/.gitkeep  
data/.gitkeep  
screenshots/.gitkeep  
tests/test_ga_core.py  

## Quick start

Install dependencies and run:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

Run core tests without opening Pygame:

PYTHONPATH=. python3 -m pytest tests

## Controls

Space pauses or resumes evolution.

N advances one generation when paused.

R resets the population.

1 loads sphere landscape.

2 loads Rastrigin landscape.

3 loads Himmelblau landscape.

4 loads ridge landscape.

5 loads multi-peak landscape.

Up and Down change mutation rate.

Right and Left change crossover rate.

E toggles elitism level.

T toggles population trails.

D toggles debug overlay.

S saves a screenshot.

Escape or Q exits.

## Educational purpose

A genetic algorithm is an optimization method inspired by evolutionary processes. A population of candidate solutions is evaluated, selected, recombined and mutated across generations. Good solutions tend to survive and spread, while mutation preserves exploration.

This project explains the algorithm visually. The population moves across a fitness landscape, and the user can see convergence, diversity loss, local optima and the effect of mutation and crossover.

## Portfolio value

The strongest portfolio angle is the direct implementation of the evolutionary pipeline. The project demonstrates algorithmic modeling, optimization, visualization, runtime parameter control, Pygame rendering, documentation and tests.

## Responsible reconstruction note

This is a reconstructed educational visualizer. It should be presented as a clean baseline, not as a recovered full historical source tree.
