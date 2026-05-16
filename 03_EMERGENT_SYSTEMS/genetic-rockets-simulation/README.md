# Genetic Rockets Simulation

This repository is a clean reconstructed skeleton of the old Genetic Algorithm Rockets simulation. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project demonstrates a genetic algorithm through a Pygame simulation where small rockets evolve over generations in order to reach a target while avoiding an obstacle. Each rocket contains a DNA sequence made of force vectors. The population is evaluated at the end of each generation, the best candidates are selected, crossover creates new DNA, and mutation introduces controlled variation.

The visual goal is simple and effective: the first generations behave randomly, while later generations begin to discover better trajectories. This makes the genetic algorithm visible as an emergent optimization process rather than only as abstract theory.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Simulation type: Pygame educational genetic algorithm  
Hardware validation: not applicable  
Algorithm validation: basic evolutionary loop included  
Portfolio readiness: prepared baseline  
Screenshots: supported through runtime command  

## Features

The simulation includes a real population loop, rocket DNA, crossover, mutation, tournament selection, generation statistics, target detection, obstacle collision, pause/reset controls and screenshot export.

The DNA model is intentionally robust and readable. Each gene is a two-dimensional acceleration vector. During a generation, every rocket reads one gene per frame and applies it as thrust. At the end of the lifespan, the population is evaluated and a new generation is created.

Fitness rewards rockets that get close to the target. Completed rockets receive a strong bonus, and rockets that reach the target earlier receive an additional speed bonus. Crashed rockets receive a penalty.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
genetic_rockets/dna.py  
genetic_rockets/rocket.py  
genetic_rockets/obstacle.py  
genetic_rockets/population.py  
genetic_rockets/app.py  
docs/genetic_algorithm_notes.md  
docs/controls_and_usage.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_dna_vector_model.md  
issues/002_screenshot_gallery.md  
labels/repo_labels.md  
screenshots/.gitkeep  
data/.gitkeep  
tests/test_dna.py  

## Quick start

Create a virtual environment if desired, install the dependencies and run the simulation.

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

## Controls

Space pauses or resumes the simulation.  
R resets the population and generation counter.  
S saves a screenshot into the screenshots folder.  
H toggles the help overlay.  
O creates a new random obstacle.  
C restores the default obstacle.  
Up increases mutation rate.  
Down decreases mutation rate.  
Escape exits the application.

## Educational purpose

This project is designed to explain the basic structure of a genetic algorithm: representation, evaluation, selection, crossover and mutation.

The representation is the DNA vector sequence. The evaluation is the fitness score. Selection chooses better candidates more often. Crossover combines two parent DNA sequences. Mutation introduces random exploration so that the population does not become stuck too early.

The project can also be conceptually linked to MicroBot simulation work. A future MicroBot swarm simulator could use similar evolutionary techniques to optimize movement patterns, docking paths, formation strategies or navigation policies in simulated environments.

## Notes

This repository is intentionally small, clean and readable. It should be treated as a reconstructed educational baseline, not as a recovered full historical source tree.
