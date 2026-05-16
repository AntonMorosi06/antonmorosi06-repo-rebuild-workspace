import numpy as np

from dbscan_pygame_visualizer.dbscan_core import NOISE, dbscan


def test_dbscan_finds_two_clusters_and_noise():
    points = np.array([
        [0.0, 0.0],
        [0.5, 0.0],
        [0.0, 0.5],
        [20.0, 20.0],
        [20.5, 20.0],
        [20.0, 20.5],
        [100.0, 100.0],
    ])

    result = dbscan(points, eps=1.2, min_samples=3)

    assert result.cluster_count == 2
    assert result.noise_count == 1
    assert result.labels[-1] == NOISE


def test_dbscan_empty_dataset():
    points = np.zeros((0, 2), dtype=float)
    result = dbscan(points, eps=10.0, min_samples=3)

    assert result.cluster_count == 0
    assert result.noise_count == 0
    assert len(result.labels) == 0


def test_dbscan_rejects_invalid_eps():
    points = np.array([[0.0, 0.0]])

    try:
        dbscan(points, eps=0.0, min_samples=1)
    except ValueError as exc:
        assert "eps" in str(exc)
    else:
        raise AssertionError("dbscan should reject eps <= 0")
