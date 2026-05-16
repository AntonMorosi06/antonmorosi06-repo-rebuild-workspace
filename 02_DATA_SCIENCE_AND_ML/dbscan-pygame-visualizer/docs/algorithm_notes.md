# DBSCAN algorithm notes

DBSCAN stands for Density-Based Spatial Clustering of Applications with Noise. The algorithm starts from the idea that a cluster is not necessarily spherical, centered, or predefined. A cluster is a region where points are sufficiently dense according to two parameters.

The first parameter is eps. It defines the radius of the neighborhood around a point. The second parameter is min_samples. It defines how many points must be inside that radius for the point to be treated as a core point.

A core point is a point with enough neighbors. A border point is not dense enough by itself, but it is close to at least one core point. A noise point is neither a core point nor reachable from a core point.

The implementation in this repository computes the pairwise distance matrix with NumPy, builds a neighborhood list for every point, identifies core points, then expands clusters by walking from core point to core point. Points previously marked as noise can later be absorbed into a cluster if they become density-reachable from a valid core region.

This version is intentionally readable rather than optimized for huge datasets. It is appropriate for educational visualization, portfolio explanation, and small interactive experiments.
