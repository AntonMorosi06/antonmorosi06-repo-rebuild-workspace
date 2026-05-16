# Algorithm walkthrough

The reconstructed implementation follows the standard DBSCAN logic.

First, every raw point is wrapped into a ClusteredPoint object.

The algorithm iterates through all points. If a point has already been visited, it is skipped.

For an unvisited point, the algorithm finds all neighbors within epsilon.

If the number of neighbors is smaller than min_samples, the point is temporarily labeled as noise.

If the point has enough neighbors, a new cluster is created. The algorithm expands that cluster by visiting neighbors, finding their neighbors and adding density-reachable points.

At the end, points inside clusters are classified as core or border. Points still labeled as noise remain noise.
