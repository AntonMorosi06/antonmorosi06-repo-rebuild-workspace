# PCA Explanation

Principal Component Analysis is a technique used to identify the main directions of variance inside a dataset.

In a 3D point cloud, PCA finds three orthogonal directions:

- PC1, the direction where the data varies the most;
- PC2, the second strongest direction of variation;
- PC3, the remaining orthogonal direction.

The algorithm used here is:

1. Generate or load points.
2. Center the data by subtracting the mean.
3. Compute the covariance matrix.
4. Compute eigenvalues and eigenvectors.
5. Sort eigenvectors by descending eigenvalue.
6. Draw those vectors as principal axes.

This project uses NumPy directly instead of scikit-learn because the goal is educational transparency.
