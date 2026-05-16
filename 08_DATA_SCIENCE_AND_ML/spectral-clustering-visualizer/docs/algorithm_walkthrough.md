# Algorithm walkthrough

The reconstructed implementation follows this pipeline.

First, the dataset is generated or loaded.

Second, a Gaussian affinity matrix is computed from pairwise distances.

Third, the graph can be sparsified with a k-nearest-neighbor rule.

Fourth, the degree vector is computed.

Fifth, the normalized graph Laplacian is built.

Sixth, the smallest eigenvectors of the Laplacian are computed with a Jacobi eigen decomposition.

Seventh, the first k eigenvectors are used as the spectral embedding.

Eighth, each embedding row is normalized.

Finally, k-means clusters the embedded points.
