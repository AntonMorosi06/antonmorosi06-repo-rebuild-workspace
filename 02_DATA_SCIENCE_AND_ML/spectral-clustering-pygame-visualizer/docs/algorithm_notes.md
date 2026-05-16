# Spectral clustering algorithm notes

Spectral clustering treats a dataset as a graph. Each point becomes a node, and edges connect points that are similar or near one another. Instead of assuming that clusters are spherical or centroid-shaped, spectral clustering studies the structure of this graph.

The first stage is affinity construction. In this repository, each point is connected to its k nearest neighbors. The edge weight is computed with a radial basis similarity controlled by sigma. A small sigma makes distant points almost unrelated, while a larger sigma keeps wider neighborhoods connected.

The second stage is graph symmetrization. A raw k-nearest-neighbor graph can be directed because point A may select point B as a neighbor while point B may not select point A. This visualizer symmetrizes the graph by taking the maximum between the graph and its transpose. This produces an undirected affinity matrix suitable for the normalized Laplacian.

The third stage is Laplacian construction. The normalized graph Laplacian is built from the affinity matrix and the degree vector. The smallest eigenvectors of the Laplacian provide a low-dimensional embedding where graph partitions become easier to separate.

The final stage is clustering in the spectral embedding. This repository uses a small built-in k-means implementation so the visualizer remains lightweight and does not depend on scikit-learn.

This implementation is designed for educational clarity. It is appropriate for small interactive datasets, screenshots and portfolio explanation. It is not optimized for very large datasets.
