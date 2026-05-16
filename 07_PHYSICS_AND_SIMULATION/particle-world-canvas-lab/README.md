# Particle World Canvas Lab

This repository is a clean reconstructed skeleton of the old particle world / vortex / interactive particle simulation work. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements a browser-based particle simulation using static HTML, CSS and JavaScript Canvas. It includes particles, force fields, attractors, repulsors, vortex mode, gravity mode, mouse interaction, trails, presets, telemetry and runtime controls.

The project is educational and visual. It is not a physically exact solver. It uses simplified vector fields and numerical integration to make force, motion, attraction, repulsion, turbulence and emergent patterns visible.

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

The simulation includes multiple presets: calm orbit, vortex, gravity well, repulsion field, swarm drift and chaos mode.

Particles are represented with position, velocity, acceleration, mass, radius, hue, energy and trail memory.

The user can change particle count, field strength, damping, trail opacity, turbulence, mouse influence and simulation speed.

Mouse interaction can attract or repel particles depending on the selected mode.

The interface includes telemetry: particle count, average speed, average energy, preset, field mode and frame count.

## Repository layout

README.md  
CHANGELOG.md  
index.html  
style.css  
src/vector.js  
src/particle.js  
src/fields.js  
src/simulation.js  
src/renderer.js  
src/ui.js  
src/app.js  
docs/physics_model.md  
docs/visual_model.md  
docs/controls_and_usage.md  
docs/github_pages_checklist.md  
docs/browser_test_checklist.md  
docs/scientific_limitations.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_particle_performance.md  
issues/002_presets_and_export.md  
issues/003_future_microbot_mapping.md  
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

B creates a burst.

T toggles trails.

D toggles debug overlay.

1 selects calm orbit.

2 selects vortex.

3 selects gravity well.

4 selects repulsion field.

5 selects swarm drift.

6 selects chaos mode.

The sliders control particle count, field strength, damping, turbulence, trail opacity, mouse influence and speed.

## Responsible scientific framing

This is a simplified visual simulation. It is useful for studying qualitative behavior, vector fields, emergent motion and creative coding. It should not be presented as a precise physical solver.

## MicroBot connection

This project can later become a visual sandbox for MicroBot swarm states: particles can represent agents, attractors can represent goals, repulsors can represent obstacles, and vector fields can represent communication gradients, energy maps or environmental forces.
