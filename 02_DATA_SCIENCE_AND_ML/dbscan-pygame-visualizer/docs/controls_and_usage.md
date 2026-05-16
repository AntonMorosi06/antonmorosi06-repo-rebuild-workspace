# Controls and usage

Run the project with:

python3 main.py

The interface opens a Pygame window with the clustering canvas on the left and the dashboard on the right.

Left mouse click adds a new point to the canvas.

R regenerates a synthetic dataset with multiple Gaussian-like clusters and noise.

C clears the dataset.

N adds random noise points.

Plus and minus increase or decrease eps.

Left bracket and right bracket decrease or increase min_samples.

Space forces a recomputation.

S saves a screenshot into the screenshots directory.

H toggles the help overlay.

Escape exits the visualizer.

The dirty-state flag avoids unnecessary recomputation. Whenever the point set, eps, or min_samples changes, the state becomes dirty. The next frame recomputes DBSCAN and then marks the state as clean again.
