from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class SpectralResult:
    labels: np.ndarray
    affinity: np.ndarray
    degree: np.ndarray
    laplacian: np.ndarray
    eigenvalues: np.ndarray
    embedding: np.ndarray
    cluster_count: int
    neighbor_count: int
    sigma: float

    @property
    def edge_count(self) -> int:
        if self.affinity.size == 0:
            return 0
        upper = np.triu(self.affinity > 0, k=1)
        return int(np.sum(upper))


def pairwise_squared_distances(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be a NumPy array with shape (n, 2)")
    if len(points) == 0:
        return np.zeros((0, 0), dtype=float)
    delta = points[:, None, :] - points[None, :, :]
    return np.sum(delta * delta, axis=2)


def build_knn_affinity(points: np.ndarray, neighbor_count: int, sigma: float) -> np.ndarray:
    points = np.asarray(points, dtype=float)

    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be a NumPy array with shape (n, 2)")
    if neighbor_count < 1:
        raise ValueError("neighbor_count must be at least 1")
    if sigma <= 0:
        raise ValueError("sigma must be positive")

    n = len(points)
    if n == 0:
        return np.zeros((0, 0), dtype=float)

    distances_sq = pairwise_squared_distances(points)
    affinity = np.zeros((n, n), dtype=float)
    max_neighbors = min(neighbor_count, max(0, n - 1))

    if max_neighbors == 0:
        return affinity

    denominator = 2.0 * sigma * sigma

    for index in range(n):
        order = np.argsort(distances_sq[index])
        candidates = [candidate for candidate in order if candidate != index][:max_neighbors]
        for candidate in candidates:
            weight = float(np.exp(-distances_sq[index, candidate] / denominator))
            affinity[index, candidate] = weight

    affinity = np.maximum(affinity, affinity.T)
    np.fill_diagonal(affinity, 0.0)
    return affinity


def normalized_laplacian(affinity: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    affinity = np.asarray(affinity, dtype=float)

    if affinity.ndim != 2 or affinity.shape[0] != affinity.shape[1]:
        raise ValueError("affinity must be a square matrix")

    degree = np.sum(affinity, axis=1)
    safe_degree = np.where(degree > 1e-12, degree, 1.0)
    inv_sqrt_degree = 1.0 / np.sqrt(safe_degree)
    normalized_affinity = affinity * inv_sqrt_degree[:, None] * inv_sqrt_degree[None, :]
    laplacian = np.eye(len(affinity), dtype=float) - normalized_affinity
    return laplacian, degree


def row_normalize(matrix: np.ndarray) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=float)
    if matrix.size == 0:
        return matrix
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    safe_norms = np.where(norms > 1e-12, norms, 1.0)
    return matrix / safe_norms


def kmeans(data: np.ndarray, k: int, iterations: int = 40, seed: int = 7) -> np.ndarray:
    data = np.asarray(data, dtype=float)

    if data.ndim != 2:
        raise ValueError("data must be a 2D matrix")
    if k < 1:
        raise ValueError("k must be at least 1")

    n = len(data)
    if n == 0:
        return np.array([], dtype=int)

    k = min(k, n)
    rng = np.random.default_rng(seed)

    first_index = int(rng.integers(0, n))
    centers = [data[first_index]]

    while len(centers) < k:
        center_matrix = np.vstack(centers)
        distances = np.sum((data[:, None, :] - center_matrix[None, :, :]) ** 2, axis=2)
        closest = np.min(distances, axis=1)
        next_index = int(np.argmax(closest))
        centers.append(data[next_index])

    centers = np.vstack(centers)
    labels = np.zeros(n, dtype=int)

    for _ in range(iterations):
        distances = np.sum((data[:, None, :] - centers[None, :, :]) ** 2, axis=2)
        new_labels = np.argmin(distances, axis=1)

        if np.array_equal(labels, new_labels):
            break

        labels = new_labels

        for cluster_id in range(k):
            members = data[labels == cluster_id]
            if len(members) == 0:
                centers[cluster_id] = data[int(rng.integers(0, n))]
            else:
                centers[cluster_id] = np.mean(members, axis=0)

    return labels.astype(int)


def spectral_cluster(
    points: np.ndarray,
    cluster_count: int,
    neighbor_count: int,
    sigma: float,
) -> SpectralResult:
    points = np.asarray(points, dtype=float)

    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be a NumPy array with shape (n, 2)")
    if cluster_count < 1:
        raise ValueError("cluster_count must be at least 1")
    if neighbor_count < 1:
        raise ValueError("neighbor_count must be at least 1")
    if sigma <= 0:
        raise ValueError("sigma must be positive")

    n = len(points)
    if n == 0:
        return SpectralResult(
            labels=np.array([], dtype=int),
            affinity=np.zeros((0, 0), dtype=float),
            degree=np.array([], dtype=float),
            laplacian=np.zeros((0, 0), dtype=float),
            eigenvalues=np.array([], dtype=float),
            embedding=np.zeros((0, 0), dtype=float),
            cluster_count=0,
            neighbor_count=int(neighbor_count),
            sigma=float(sigma),
        )

    effective_clusters = min(int(cluster_count), n)

    affinity = build_knn_affinity(points, neighbor_count=neighbor_count, sigma=sigma)
    laplacian, degree = normalized_laplacian(affinity)

    eigenvalues, eigenvectors = np.linalg.eigh(laplacian)
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    embedding = eigenvectors[:, :effective_clusters]
    embedding = row_normalize(embedding)

    labels = kmeans(embedding, effective_clusters)

    return SpectralResult(
        labels=labels,
        affinity=affinity,
        degree=degree,
        laplacian=laplacian,
        eigenvalues=eigenvalues[: min(8, len(eigenvalues))],
        embedding=embedding,
        cluster_count=effective_clusters,
        neighbor_count=int(neighbor_count),
        sigma=float(sigma),
    )
