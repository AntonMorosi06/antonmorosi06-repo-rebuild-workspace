# Known limitations

This is an educational visualizer, not a production clustering library.

The current implementation computes a full pairwise distance matrix and a full eigen-decomposition. This is simple and readable, but it is not suitable for very large datasets.

The k-means stage is intentionally small and local. It is enough for this educational visualizer but does not include every feature of a mature machine learning library.

The current app supports only two-dimensional point placement because the purpose is interactive visualization in Pygame.

The project does not currently load external CSV datasets. That can be added later through a loader and coordinate normalization layer.

The visualizer intentionally avoids claiming hardware validation, production analytics validation or recovered historical source equivalence.
