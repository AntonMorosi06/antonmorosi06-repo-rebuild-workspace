# Spectral clustering theory

Spectral clustering treats the dataset as a graph.

Each data point becomes a node. Edges connect similar points. The similarity can be computed with a Gaussian kernel, where nearby points receive high similarity and distant points receive low similarity.

From the similarity graph, the algorithm builds a degree vector and a graph Laplacian. The Laplacian describes connectivity structure in the graph.

The smallest eigenvectors of the normalized Laplacian reveal low-dimensional structure related to graph cuts and connected components.

The data is then embedded into a spectral space using those eigenvectors. A final clustering algorithm, often k-means, is applied in that spectral embedding.

This method can separate non-convex shapes that are difficult for algorithms such as standard k-means in the original coordinate space.
