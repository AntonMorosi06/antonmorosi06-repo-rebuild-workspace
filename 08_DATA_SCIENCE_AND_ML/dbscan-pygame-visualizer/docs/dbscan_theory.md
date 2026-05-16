# DBSCAN theory

DBSCAN stands for Density-Based Spatial Clustering of Applications with Noise.

The algorithm groups points that belong to dense regions. It uses two main parameters: epsilon and min_samples.

Epsilon defines the radius of the neighborhood around a point.

Min_samples defines how many points must be inside that neighborhood for the point to be considered a core point.

A core point has enough neighbors to start or continue a cluster.

A border point does not have enough neighbors to be core, but it is reachable from a core point.

A noise point is not reachable from any dense region.

The main advantage is that DBSCAN can find non-spherical clusters and can identify outliers without requiring the number of clusters in advance.
