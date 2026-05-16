from dbscan_pygame_visualizer.datasets import dataset_names, generate_dataset
from dbscan_pygame_visualizer.dbscan import NOISE, dbscan, region_query
from dbscan_pygame_visualizer.metrics import cluster_size_map, result_summary
from dbscan_pygame_visualizer.point import ClusteredPoint, Point2D


def test_dataset_names_include_expected_values():
    names = dataset_names()

    assert "blobs" in names
    assert "moons" in names
    assert "rings" in names
    assert "noise" in names
    assert "mixed" in names


def test_region_query_finds_nearby_points():
    points = [
        ClusteredPoint(Point2D(0.0, 0.0)),
        ClusteredPoint(Point2D(0.1, 0.0)),
        ClusteredPoint(Point2D(2.0, 2.0)),
    ]

    neighbors = region_query(points, 0, epsilon=0.25)

    assert 0 in neighbors
    assert 1 in neighbors
    assert 2 not in neighbors


def test_dbscan_clusters_simple_groups():
    raw = [
        Point2D(0.0, 0.0),
        Point2D(0.1, 0.0),
        Point2D(0.0, 0.1),
        Point2D(5.0, 5.0),
        Point2D(5.1, 5.0),
        Point2D(5.0, 5.1),
        Point2D(10.0, 10.0),
    ]

    result = dbscan(raw, epsilon=0.25, min_samples=3)

    assert result.cluster_count == 2
    assert result.noise_count == 1
    assert result.labels()[-1] == NOISE


def test_dbscan_on_blobs_finds_clusters():
    raw = generate_dataset("blobs", seed=42)
    result = dbscan(raw, epsilon=0.42, min_samples=5)

    assert result.cluster_count >= 3
    assert result.core_count > 0


def test_result_summary_contains_cluster_sizes():
    raw = generate_dataset("blobs", seed=42)
    result = dbscan(raw, epsilon=0.42, min_samples=5)
    summary = result_summary(result)

    assert "cluster_count" in summary
    assert "cluster_sizes" in summary
    assert cluster_size_map(result)
