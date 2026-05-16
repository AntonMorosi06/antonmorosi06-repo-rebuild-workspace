import numpy as np

from spectral_clustering_pygame_visualizer.spectral_core import (
    build_knn_affinity,
    normalized_laplacian,
    spectral_cluster,
)


def test_knn_affinity_is_symmetric():
    points = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [8.0, 8.0],
    ])

    affinity = build_knn_affinity(points, neighbor_count=2, sigma=2.0)

    assert affinity.shape == (4, 4)
    assert np.allclose(affinity, affinity.T)
    assert np.allclose(np.diag(affinity), 0.0)


def test_normalized_laplacian_shape():
    points = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
    ])

    affinity = build_knn_affinity(points, neighbor_count=1, sigma=2.0)
    laplacian, degree = normalized_laplacian(affinity)

    assert laplacian.shape == (3, 3)
    assert degree.shape == (3,)


def test_spectral_cluster_returns_labels():
    points = np.array([
        [0.0, 0.0],
        [0.2, 0.0],
        [0.0, 0.2],
        [10.0, 10.0],
        [10.2, 10.0],
        [10.0, 10.2],
    ])

    result = spectral_cluster(points, cluster_count=2, neighbor_count=2, sigma=2.0)

    assert len(result.labels) == len(points)
    assert result.cluster_count == 2
    assert result.affinity.shape == (6, 6)


def test_spectral_cluster_empty_dataset():
    points = np.zeros((0, 2), dtype=float)
    result = spectral_cluster(points, cluster_count=2, neighbor_count=2, sigma=2.0)

    assert len(result.labels) == 0
    assert result.cluster_count == 0
    assert result.affinity.shape == (0, 0)
