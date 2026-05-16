# Controls and usage

Run the project with:

python3 main.py

The interface opens a Pygame window with the graph and point canvas on the left and the dashboard on the right.

Left mouse click adds a point to the canvas.

R regenerates the default two-arc manifold-like dataset.

C clears the dataset.

N adds random noise points.

J decreases the number of clusters.

K increases the number of clusters.

Left bracket decreases the number of k-nearest neighbors.

Right bracket increases the number of k-nearest neighbors.

Minus decreases the affinity sigma value.

Plus increases the affinity sigma value.

G toggles graph edge visibility.

S saves a screenshot into the screenshots directory.

H toggles the help overlay.

Space forces a recomputation.

Escape exits the visualizer.

S is used only for screenshots. This avoids the old control conflict where the same key could be interpreted as screenshot or zoom.
