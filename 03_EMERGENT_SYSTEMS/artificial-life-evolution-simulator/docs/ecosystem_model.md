# Ecosystem model

The simulator models a small artificial ecosystem. The main entities are prey, predators and food. Prey search for food, avoid predators and reproduce when their energy is high enough. Predators search for prey, gain energy by hunting and reproduce less frequently.

The simulation is local. A creature does not know the whole world. It reacts only to nearby food, nearby predators, nearby prey and world boundaries. This is important because emergent behavior becomes visible when many local decisions create global population patterns.

Energy is the central survival variable. Movement and metabolism consume energy. Food gives prey energy. Hunting gives predators energy. Reproduction costs energy because the parent gives part of its energy to the child. Death occurs when energy is depleted or when the creature exceeds its DNA-based longevity.

The environment changes over time. The day-night cycle affects the effective vision of creatures depending on nocturnality. Seasons affect food growth and metabolic pressure. Random events can create food blooms, cold snaps, predator pressure or quiet recovery moments.

The simulator uses a spatial hash to speed up local neighbor queries. Instead of checking every creature against every other creature all the time, the world partitions space into cells and asks only for objects near a creature. This keeps the system readable while preparing it for larger populations.
