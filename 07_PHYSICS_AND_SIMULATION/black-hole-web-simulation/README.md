# Black Hole Web Simulation

This repository is a clean reconstructed skeleton of the old web-based black hole simulation project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements a browser-based black-hole-inspired visual simulation using HTML, CSS and JavaScript Canvas. It includes a central event horizon, accretion disk particles, simplified gravitational attraction, orbital trails, absorption shockwaves, polar jets, lensing-style distortion rings, runtime controls and telemetry panels.

This project is educational and visual. It does not claim to be a numerically accurate astrophysical simulator. It uses simplified force fields and visual heuristics to communicate ideas such as attraction, orbit, accretion, absorption, emission and field distortion.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Project type: static HTML/CSS/JS simulation  
Main technology: Canvas 2D  
External dependencies: none  
Physics claim: simplified educational visualization  
Portfolio readiness: prepared baseline  
GitHub Pages readiness: prepared baseline  

## Features

The page includes a full-screen canvas simulation, particle system, event horizon, accretion disk, gravitational field rings, absorption shockwaves, polar jets, runtime controls, spawn modes, parameter sliders, pause/reset, screenshot instructions and technical telemetry.

The simulation can run directly in the browser with no build step. It is suitable for GitHub Pages deployment.

## Repository layout

README.md  
CHANGELOG.md  
index.html  
style.css  
src/vector.js  
src/particle.js  
src/simulation.js  
src/renderer.js  
src/ui.js  
src/app.js  
docs/physics_model.md  
docs/visual_model.md  
docs/scientific_limitations.md  
docs/controls_and_usage.md  
docs/github_pages_checklist.md  
docs/browser_test_checklist.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_parameter_tuning.md  
issues/002_visual_export_and_gallery.md  
issues/003_future_threejs_version.md  
labels/repo_labels.md  
assets/img/.gitkeep  
data/.gitkeep  
screenshots/.gitkeep  
tests/static_file_check.py  

## Quick start

Open index.html directly in a browser, or serve the folder locally:

python3 -m http.server 8080

Then open:

http://127.0.0.1:8080

## Controls

Space pauses or resumes the simulation.

R resets the simulation.

B creates a particle burst.

J toggles polar jets.

T toggles trails.

D toggles debug overlay.

1 selects edge spawn mode.

2 selects disk spawn mode.

3 selects spiral spawn mode.

4 selects rain spawn mode.

5 selects cluster spawn mode.

The sliders control mass, particle count, trail opacity, disk energy and lensing intensity.

## Responsible scientific framing

This is not a real general relativity simulator. It does not solve Einstein field equations, relativistic geodesics, plasma dynamics or physically accurate ray tracing. It is a visual and educational approximation.

## Portfolio value

The project demonstrates static web architecture, Canvas animation, vector math, particle systems, runtime UI controls, scientific communication and responsible limitation framing.
