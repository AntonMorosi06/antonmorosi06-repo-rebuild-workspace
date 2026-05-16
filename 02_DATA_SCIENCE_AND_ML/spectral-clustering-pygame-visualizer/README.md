# Spectral Clustering Pygame Visualizer

This repository is a clean reconstructed skeleton of the old Spectral Clustering Pygame demo. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The goal of this project is to provide an interactive visual explanation of spectral clustering, graph affinity, k-nearest-neighbor connectivity, eigenvector embeddings and cluster separation. Unlike simple centroid-based methods, spectral clustering first transforms the dataset into a graph and then clusters points according to graph structure.

This project is useful as a portfolio-ready educational demo for machine learning, graph-based clustering, data visualization, algorithmic thinking and future MicroBot telemetry experiments. In a MicroBot context, the same conceptual model can be used to reason about local communication graphs, neighborhood connectivity, swarm formations, sensor affinity and distributed structure detection.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Hardware validation: not applicable  
Algorithm validation: local NumPy implementation included  
Portfolio readiness: prepared baseline  
Screenshots: supported through the runtime interface  

## Features

The visualizer contains a real local spectral clustering implementation based on NumPy. It builds a k-nearest-neighbor affinity graph, symmetrizes the graph, computes the normalized graph Laplacian, extracts the smallest eigenvectors and clusters the resulting spectral embedding with a small built-in k-means routine.

The Pygame interface allows the user to add points, regenerate synthetic datasets, tune the number of clusters, tune the number of graph neighbors, tune the affinity sigma value, toggle graph edges and save screenshots.

The project also uses a dirty-state flag. Spectral clustering is recalculated only when points or parameters change. This avoids recomputing the eigen-decomposition continuously on every rendered frame.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
spectral_clustering_pygame_visualizer/spectral_core.py  
spectral_clustering_pygame_visualizer/datasets.py  
spectral_clustering_pygame_visualizer/app.py  
docs/algorithm_notes.md  
docs/controls_and_usage.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_knn_graph_symmetrization.md  
issues/002_screenshot_gallery.md  
labels/repo_labels.md  
screenshots/.gitkeep  
data/.gitkeep  
tests/test_spectral_core.py  

## Quick start

Create a virtual environment if desired, install the dependencies and run the visualizer.

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

## Controls

Left mouse click adds a point.  
R regenerates the default manifold-like dataset.  
C clears the canvas.  
N adds random noise points.  
J and K decrease or increase the number of clusters.  
Left bracket and right bracket decrease or increase the k-nearest-neighbor graph degree.  
Minus and plus decrease or increase the affinity sigma value.  
G toggles graph edge visibility.  
H toggles the help overlay.  
S saves a screenshot into the screenshots folder.  
Space forces a recalculation.  
Escape exits the application.

## Educational purpose

Spectral clustering is useful when clusters are not easily separable by simple Euclidean centroids. It builds a graph of point relationships, studies the structure of that graph through the Laplacian matrix and uses eigenvectors to reveal hidden partitions.

In this visualizer, the graph edges make the affinity structure visible. The clustering result depends strongly on the neighborhood graph and the sigma parameter. This helps the user understand why spectral clustering is powerful but also parameter-sensitive.

## Notes

This repository is intentionally small, clean and readable. It should be treated as a reconstructed educational baseline, not as a recovered full historical source tree.
