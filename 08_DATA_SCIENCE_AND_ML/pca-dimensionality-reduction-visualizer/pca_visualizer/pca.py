from __future__ import annotations

from dataclasses import dataclass

from .linalg import Matrix, Vector, add, center_data, covariance_matrix, dot, jacobi_eigen_symmetric, mean_vector, scale


@dataclass
class PCAResult:
    mean: Vector
    covariance: Matrix
    eigenvalues: Vector
    components: Matrix
    explained_variance_ratio: Vector
    centered: Matrix
    transformed: Matrix
    reconstructed: Matrix
    n_components: int

    @property
    def total_variance(self) -> float:
        return sum(max(0.0, value) for value in self.eigenvalues)

    @property
    def retained_variance_ratio(self) -> float:
        return sum(self.explained_variance_ratio[: self.n_components])


def fit_pca(data: Matrix, n_components: int | None = None) -> PCAResult:
    if not data:
        raise ValueError("data cannot be empty")

    dimension = len(data[0])
    if any(len(row) != dimension for row in data):
        raise ValueError("all rows must have the same dimension")

    if n_components is None:
        n_components = min(2, dimension)

    n_components = max(1, min(dimension, n_components))

    mean = mean_vector(data)
    centered = center_data(data, mean)
    covariance = covariance_matrix(centered)
    eigenvalues, components = jacobi_eigen_symmetric(covariance)

    total = sum(max(0.0, value) for value in eigenvalues)
    if total <= 1e-12:
        explained = [0.0 for _ in eigenvalues]
    else:
        explained = [max(0.0, value) / total for value in eigenvalues]

    transformed = transform_centered(centered, components, n_components)
    reconstructed = inverse_transform(transformed, components, mean, n_components)

    return PCAResult(
        mean=mean,
        covariance=covariance,
        eigenvalues=eigenvalues,
        components=components,
        explained_variance_ratio=explained,
        centered=centered,
        transformed=transformed,
        reconstructed=reconstructed,
        n_components=n_components,
    )


def transform_centered(centered: Matrix, components: Matrix, n_components: int) -> Matrix:
    selected = components[:n_components]
    return [[dot(row, component) for component in selected] for row in centered]


def transform(data: Matrix, result: PCAResult, n_components: int | None = None) -> Matrix:
    n_components = n_components or result.n_components
    centered = center_data(data, result.mean)
    return transform_centered(centered, result.components, n_components)


def inverse_transform(transformed: Matrix, components: Matrix, mean: Vector, n_components: int) -> Matrix:
    selected = components[:n_components]
    reconstructed: Matrix = []

    for row in transformed:
        rebuilt = [0.0 for _ in mean]
        for score, component in zip(row, selected):
            rebuilt = add(rebuilt, scale(component, score))
        reconstructed.append(add(rebuilt, mean))

    return reconstructed
