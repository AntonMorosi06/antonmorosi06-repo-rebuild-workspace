# PCA Dimensionality Reduction Visualizer

This repository is a clean reconstructed skeleton of the old PCA / dimensionality-reduction visualizer project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements an educational Principal Component Analysis visualizer using Python and Pygame. The PCA algorithm is implemented directly in the repository, including centering, covariance matrix construction, Jacobi eigen decomposition, explained variance ratio and projection into principal-component coordinates.

The architecture separates the PCA core from the Pygame interface. The mathematical logic can be tested without opening a graphical window.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Project type: data science / machine learning visualization  
Algorithm: PCA implemented from scratch  
Interface: Pygame  
Core engine: pure Python and testable without Pygame  
External ML dependency: none  
Portfolio readiness: prepared baseline  

## Features

The visualizer includes synthetic datasets such as correlated 2D cloud, elongated ellipse, rotated clusters, 3D ribbon projected into PCA space and noisy line.

The Pygame interface shows the original data, centered data, principal axes, projected coordinates, explained variance ratio and reconstruction error for a selected number of components.

The user can switch datasets, toggle centered view, toggle projected view, change number of components, regenerate data, display vectors, save screenshots and inspect PCA metrics.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
pca_visualizer/linalg.py  
pca_visualizer/datasets.py  
pca_visualizer/pca.py  
pca_visualizer/metrics.py  
pca_visualizer/palette.py  
pca_visualizer/pygame_app.py  
pca_visualizer/launcher.py  
docs/pca_theory.md  
docs/algorithm_walkthrough.md  
docs/controls_and_usage.md  
docs/dataset_notes.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_pca_step_visualization.md  
issues/002_dataset_import_export.md  
issues/003_3d_projection_view.md  
labels/repo_labels.md  
assets/.gitkeep  
data/.gitkeep  
screenshots/.gitkeep  
tests/test_pca_core.py  

## Quick start

Install dependencies and run:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

Run core tests without opening Pygame:

PYTHONPATH=. python3 -m pytest tests

## Controls

R regenerates the current dataset.

C toggles centered view.

P toggles projected PCA view.

V toggles principal vectors.

1 loads correlated cloud.

2 loads elongated ellipse.

3 loads rotated clusters.

4 loads 3D ribbon.

5 loads noisy line.

Up increases selected component count.

Down decreases selected component count.

D toggles debug overlay.

S saves a screenshot.

Escape or Q exits.

## Educational purpose

PCA is a dimensionality reduction method that finds directions of maximum variance in the data. It is useful for compression, visualization, denoising and understanding structure in high-dimensional datasets.

This repository explains PCA visually and mathematically. It shows what centering means, why covariance matters, how principal components are ordered and how projection changes the representation of the data.

## Portfolio value

The strongest portfolio angle is that PCA is implemented directly instead of hidden behind a library call. The project demonstrates mathematical programming, data visualization, Pygame rendering, synthetic dataset generation, documentation and tests.

## Responsible reconstruction note

This is a reconstructed educational visualizer. It should be presented as a clean baseline, not as a recovered full historical source tree.
