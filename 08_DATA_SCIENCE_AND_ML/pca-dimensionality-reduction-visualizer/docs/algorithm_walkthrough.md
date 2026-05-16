# Algorithm walkthrough

The reconstructed PCA implementation follows these steps.

First, the dataset is checked for consistent dimensionality.

Second, the mean vector is computed.

Third, every sample is centered by subtracting the mean vector.

Fourth, the covariance matrix is computed from the centered data.

Fifth, the covariance matrix is diagonalized with a Jacobi eigen decomposition method.

Sixth, eigenvalues and eigenvectors are sorted in descending order of eigenvalue.

Seventh, the centered data is projected onto the selected principal components.

Finally, the projected representation can be approximately reconstructed back into the original feature space.
