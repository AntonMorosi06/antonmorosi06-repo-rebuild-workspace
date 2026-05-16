# PCA theory

Principal Component Analysis is a linear dimensionality-reduction method.

The first step is centering the data by subtracting the mean of each feature. This is important because PCA studies variance around the center of the dataset.

The next step is building the covariance matrix. The covariance matrix describes how features vary together.

PCA then computes the eigenvectors and eigenvalues of the covariance matrix. The eigenvectors are the principal directions. The eigenvalues measure how much variance exists along those directions.

The principal components are sorted from highest variance to lowest variance.

When data is projected onto the first components, the representation keeps as much variance as possible for the selected number of dimensions.
