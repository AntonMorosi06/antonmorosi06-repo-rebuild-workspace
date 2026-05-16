# DBSCAN Pygame Visualizer

This repository is a clean reconstructed skeleton of the old DBSCAN visualizer project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements a visual and educational DBSCAN clustering laboratory using Python and Pygame. The DBSCAN algorithm is implemented directly in the repository instead of relying on scikit-learn, so the user can inspect the clustering logic, neighborhood search, core points, border points, noise points and cluster expansion behavior.

The architecture separates the clustering core from the Pygame interface. The algorithm, datasets and metrics can be tested without opening a graphical window.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Project type: data science / machine learning visualization  
Algorithm: DBSCAN implemented from scratch  
Interface: Pygame  
Core engine: pure Python and testable without Pygame  
External ML dependency: none  
Portfolio readiness: prepared baseline  

## Features

The visualizer includes synthetic datasets such as blobs, moons, rings, random noise and mixed clusters.

The DBSCAN parameters epsilon and min_samples can be changed at runtime.

The visualization shows cluster colors, noise points, core points, border points, selected point neighborhoods and algorithm summary metrics.

The Pygame app includes dataset switching, parameter controls, reset, recluster, screenshot export and debug overlay.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
dbscan_pygame_visualizer/point.py  
dbscan_pygame_visualizer/datasets.py  
dbscan_pygame_visualizer/dbscan.py  
dbscan_pygame_visualizer/metrics.py  
dbscan_pygame_visualizer/palette.py  
dbscan_pygame_visualizer/pygame_app.py  
dbscan_pygame_visualizer/launcher.py  
docs/dbscan_theory.md  
docs/algorithm_walkthrough.md  
docs/controls_and_usage.md  
docs/dataset_notes.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_algorithm_step_mode.md  
issues/002_dataset_gallery.md  
issues/003_performance_neighbor_search.md  
labels/repo_labels.md  
assets/.gitkeep  
data/.gitkeep  
screenshots/.gitkeep  
tests/test_dbscan_core.py  

## Quick start

Install dependencies and run:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

Run core tests without opening Pygame:

PYTHONPATH=. python3 -m pytest tests

## Controls

R reclusters the current dataset.

B loads blob dataset.

M loads moon dataset.

O loads ring dataset.

N loads random noise dataset.

X loads mixed dataset.

Up and Down increase or decrease epsilon.

Right and Left increase or decrease min_samples.

C toggles core point overlay.

H toggles neighborhood highlight.

D toggles debug overlay.

S saves a screenshot.

Escape or Q exits.

## Educational purpose

DBSCAN is useful because it does not require the number of clusters in advance. It groups dense regions and labels sparse points as noise. This makes it different from k-means and useful for non-spherical shapes.

This repository explains DBSCAN through code and visualization. The goal is not only to run clustering, but to see why points become core, border or noise points.

## Portfolio value

The strongest portfolio angle is the combination of algorithmic clarity and visual explanation. The project shows Python data modeling, clustering logic, synthetic dataset generation, Pygame rendering, parameter exploration, documentation and tests.

## Responsible reconstruction note

This is a reconstructed educational visualizer. It should be presented as a clean baseline, not as a recovered full historical source tree.
