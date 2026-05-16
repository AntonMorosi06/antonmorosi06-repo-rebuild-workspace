# DBSCAN Pygame Visualizer

This repository is a clean reconstructed skeleton of the old DBSCAN Pygame demo. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The goal of this project is to provide an interactive visual explanation of DBSCAN, a density-based clustering algorithm that groups points according to local neighborhood density. Unlike k-means, DBSCAN does not require the user to choose the number of clusters in advance. It identifies dense regions as clusters and marks sparse isolated points as noise.

This project is useful as a portfolio-ready educational demo for data science, machine learning visualization, algorithmic thinking, and future MicroBot telemetry experiments. In the MicroBot context, the same conceptual model can be reused to reason about spatial telemetry, local swarm density, anomaly points, sensor clusters, and simulated formations.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Hardware validation: not applicable  
Algorithm validation: basic local DBSCAN implementation included  
Portfolio readiness: prepared baseline  
Screenshots: supported through the runtime interface  

## Features

The visualizer contains a real local DBSCAN implementation based on NumPy. The Pygame interface allows the user to add points, regenerate synthetic datasets, tune eps and min_samples, mark noise points, show core samples, and save screenshots.

The implementation also uses a dirty-state flag. This means the DBSCAN computation is recalculated only when points or parameters change, instead of being recomputed continuously every frame. This keeps the visualizer responsive and makes the code easier to reason about.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
dbscan_pygame_visualizer/dbscan_core.py  
dbscan_pygame_visualizer/datasets.py  
dbscan_pygame_visualizer/app.py  
docs/algorithm_notes.md  
docs/controls_and_usage.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_dirty_state_and_performance.md  
issues/002_screenshot_gallery.md  
labels/repo_labels.md  
screenshots/.gitkeep  
data/.gitkeep  
tests/test_dbscan_core.py  

## Quick start

Create a virtual environment if desired, install the dependencies, and run the visualizer.

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

## Controls

Left mouse click adds a point.  
R regenerates the default clustered dataset.  
C clears the canvas.  
N adds random noise points.  
Plus and minus modify eps.  
Left bracket and right bracket modify min_samples.  
H toggles the help overlay.  
S saves a screenshot into the screenshots folder.  
Space forces a recalculation.  
Escape exits the application.

## Educational purpose

DBSCAN is especially useful when clusters have irregular shapes and when the dataset contains outliers. The algorithm depends mainly on two parameters: eps, which defines the neighborhood radius, and min_samples, which defines how many nearby points are required to consider a point dense enough to become a core point.

In this visualizer, core points are emphasized, border points inherit the cluster of nearby core points, and noise points remain visually separated. This makes the density logic much easier to understand than reading the algorithm only as pseudocode.

## Notes

This repository is intentionally small, clean, and readable. It should be treated as a reconstructed educational baseline, not as a recovered full historical source tree.
