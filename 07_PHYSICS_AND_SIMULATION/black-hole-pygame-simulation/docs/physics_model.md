# Physics model

The simulation uses a simplified gravity-like attraction model.

Particles are attracted toward a central point representing the black hole. The attraction is computed using an inverse-square-style force with a softening constant to avoid infinite acceleration near the center.

A perpendicular swirl term is added to produce accretion-disk-like orbital motion. This is a visual heuristic, not a relativistic model.

Particles crossing the absorption radius are marked as absorbed and generate shockwaves. The simulation then respawns particles to keep the scene active.

This model is useful for visual intuition and creative coding, but it is not a scientific black hole solver.
