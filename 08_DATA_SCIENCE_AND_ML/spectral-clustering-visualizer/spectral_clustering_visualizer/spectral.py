from __future__ import annotations

from dataclasses import dataclass

from .graph import gaussian_affinity, graph_edges_for_display, normalized_laplacian, sparsify_knn
from .kmeans import kmeans
from .linalg import Matrix, jacobi_eigen_symmetric, row_normalize


@dataclass
class SpectralClusteringResult:
    data: Matrix
    labels: list[int]
    affinity: Matrix
    laplacian: Matrix
    eigenvalues: list[float]
    eigenvectors: Matrix
    embedding: Matrix
    centers: Matrix
    k: int
    sigma: float
    k_neighbors: int | None

    @property
    def cluster_count(self) -> int:
        return len(set(self.labels))

    def display_edges(self, threshold: float = 0.58, max_edges: int = 520) -> list[tuple[int, int, float]]:
        return graph_edges_for_display(self.data, self.affinity, threshold=threshold, max_edges=max_edges)


def spectral_clustering(
    data: Matrix,
    k: int = 2,
    sigma: float = 0.45,
    k_neighbors: int | None = 12,
    seed: int = 42,
) -> SpectralClusteringResult:
    if not data:
        raise ValueError("data cannot be empty")
    if k < 1:
        raise ValueError("k must be at least 1")
    if k > len(data):
        raise ValueError("k cannot exceed number of samples")

    affinity = gaussian_affinity(data, sigma=sigma)
    affinity = sparsify_knn(affinity, k_neighbors=k_neighbors)
    laplacian = normalized_laplacian(affinity)
    eigenvalues, eigenvectors = jacobi_eigen_symmetric(laplacian)

    selected_vectors = eigenvectors[:k]
    embedding = transpose_embedding(selected_vectors)
    embedding = row_normalize(embedding)

    labels, centers = kmeans(embedding, k=k, seed=seed)

    return SpectralClusteringResult(
        data=data,
        labels=labels,
        affinity=affinity,
        laplacian=laplacian,
        eigenvalues=eigenvalues,
        eigenvectors=eigenvectors,
        embedding=embedding,
        centers=centers,
        k=k,
        sigma=sigma,
        k_neighbors=k_neighbors,
    )


def transpose_embedding(selected_vectors: Matrix) -> Matrix:
    if not selected_vectors:
        return []

    n = len(selected_vectors[0])
    return [
        [vector[index] for vector in selected_vectors]
        for index in range(n)
    ]
