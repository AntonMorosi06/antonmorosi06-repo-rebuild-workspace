# PCA Pygame Visualizer

PCA Pygame Visualizer is a reconstructed and cleaned interactive mathematical visualization inspired by the original `AntonMorosi2234/PCA_DEMO_PYGAME` repository.

This version is not cloned from the old repository. It is rebuilt as a clean skeleton based on the previous analysis: a 3D point cloud, Principal Component Analysis computed with NumPy, principal axes, explained variance, camera rotation, zoom, regenerated datasets, screenshot export and a clear educational layout.

## Current status

Status: reconstructed functional skeleton.

This project contains:

- an interactive Pygame application in `src/pca_demo_pygame.py`;
- a correlated synthetic 3D dataset generator;
- PCA calculation with NumPy;
- visualized principal axes;
- explained variance display;
- camera controls;
- screenshot export;
- documentation;
- issue backlog;
- labels.

## What this project does

The demo generates a correlated 3D point cloud and computes Principal Component Analysis. It then visualizes:

- the point cloud;
- the coordinate axes;
- the PCA principal directions;
- the explained variance ratio;
- simple camera rotation and zoom.

## Why this matters

PCA is one of the most important tools for understanding high-dimensional data. In this project it is not hidden inside a notebook. It is shown interactively as geometry: points, axes, orientation, projection and variance.

This connects well with the broader Anton Morosi portfolio because it sits between mathematics, data science, visualization and future MicroBot telemetry analysis.

## Install

From this folder:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Run

    python src/pca_demo_pygame.py

## Controls

Mouse drag:
Rotate the camera.

Mouse wheel:
Zoom in and out.

SPACE:
Toggle PCA vectors.

R:
Regenerate correlated dataset.

C:
Reset camera.

S:
Save screenshot to `output/`.

1:
Use fixed point color mode.

2:
Use depth color mode.

3:
Use quadrant color mode.

ESC:
Exit.

## Portfolio positioning

This project demonstrates mathematical visualization, NumPy, Pygame, interactive controls and educational data-science communication. It is a compact project, but it is strong because it turns a mathematical concept into an interactive visual system.
