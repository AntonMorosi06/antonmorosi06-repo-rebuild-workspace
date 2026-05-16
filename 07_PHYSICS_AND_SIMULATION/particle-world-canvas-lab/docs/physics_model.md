# Physics model

The model uses simplified vector fields.

Particles have position, velocity, acceleration, mass, radius, energy and trails. At each frame the simulation computes a central force, a mouse force and a turbulence force. These forces are applied to acceleration, then integrated into velocity and position.

The central field can behave like a calm orbit, vortex, gravity well, repulsion field, swarm drift or chaotic flow.

This is not a precise physical solver. The purpose is to make vector-field behavior visible and interactive.
