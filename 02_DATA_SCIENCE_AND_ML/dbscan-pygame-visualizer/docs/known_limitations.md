# Known limitations

This is an educational visualizer, not a production clustering library.

The current DBSCAN implementation uses a full pairwise distance matrix. This is simple and readable, but it is not appropriate for very large datasets.

The project currently supports only two-dimensional point clouds because the goal is visual explanation inside a Pygame canvas.

The screenshot system exports runtime images but does not yet include a curated gallery.

The visualizer does not currently load external CSV datasets. This can be added later through a small data loader and coordinate normalization step.

The project intentionally avoids claiming hardware validation, production analytics validation, or recovered historical source equivalence.
