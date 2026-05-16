# Spectral Clustering Visualizer

This repository is a clean reconstructed skeleton of the old spectral clustering visualizer project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements an educational spectral clustering visualizer using Python and Pygame. The clustering pipeline is implemented directly in the repository: synthetic dataset generation, Gaussian similarity graph, optional k-nearest-neighbor sparsification, degree matrix, normalized graph Laplacian, Jacobi eigen decomposition, spectral embedding, row normalization and final k-means clustering.

The architecture separates the mathematical core from the Pygame interface. The spectral clustering pipeline can be tested without opening a graphical window.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Project type: data science / machine learning visualization  
Algorithm: spectral clustering implemented from scratch  
Interface: Pygame  
Core engine: pure Python and testable without Pygame  
External ML dependency: none  
Portfolio readiness: prepared baseline  

## Features

The visualizer includes synthetic datasets such as moons, rings, blobs, bridge graph, noisy islands and spiral arcs.

The Pygame interface shows the original data, cluster labels, similarity edges, spectral embedding preview, selected eigenvalues, parameter values and clustering summary.

The user can switch datasets, change the number of clusters, change the Gaussian sigma parameter, toggle graph edges, toggle embedding view, regenerate data and save screenshots.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
spectral_clustering_visualizer/linalg.py  
spectral_clustering_visualizer/datasets.py  
spectral_clustering_visualizer/graph.py  
spectral_clustering_visualizer/kmeans.py  
spectral_clustering_visualizer/spectral.py  
spectral_clustering_visualizer/metrics.py  
spectral_clustering_visualizer/palette.py  
spectral_clustering_visualizer/pygame_app.py  
spectral_clustering_visualizer/launcher.py  
docs/spectral_clustering_theory.md  
docs/algorithm_walkthrough.md  
docs/controls_and_usage.md  
docs/dataset_notes.md  
docs/performance_notes.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_step_by_step_pipeline.md  
issues/002_sparse_graph_performance.md  
issues/003_embedding_gallery.md  
labels/repo_labels.md  
assets/.gitkeep  
data/.gitkeep  
screenshots/.gitkeep  
tests/test_spectral_core.py  

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

1 loads moons.

2 loads rings.

3 loads blobs.

4 loads bridge.

5 loads islands.

6 loads spiral arcs.

Up increases the number of clusters.

Down decreases the number of clusters.

Right increases sigma.

Left decreases sigma.

E toggles graph edges.

P toggles spectral embedding view.

D toggles debug overlay.

S saves a screenshot.

Escape or Q exits.

## Educational purpose

Spectral clustering is useful because it transforms a dataset into a graph problem. Instead of clustering directly in the original coordinate space, it builds a similarity graph, studies the graph Laplacian and uses eigenvectors to reveal connectivity structure. This makes it effective for non-convex shapes such as moons and rings.

This repository explains spectral clustering through code and visualization. The goal is not only to produce labels, but to show how the graph and spectral embedding affect the final clusters.

## Portfolio value

The strongest portfolio angle is that the algorithm is implemented directly instead of hidden behind a library call. The project demonstrates graph construction, linear algebra, eigen decomposition, clustering, visualization, Pygame rendering, documentation and tests.

## Responsible reconstruction note

This is a reconstructed educational visualizer. It should be presented as a clean baseline, not as a recovered full historical source tree.
