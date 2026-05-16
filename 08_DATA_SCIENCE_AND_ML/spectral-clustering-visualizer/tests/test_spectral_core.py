from spectral_clustering_visualizer.datasets import dataset_names, generate_dataset
from spectral_clustering_visualizer.graph import degree_vector, gaussian_affinity, normalized_laplacian, sparsify_knn
from spectral_clustering_visualizer.kmeans import kmeans
from spectral_clustering_visualizer.linalg import jacobi_eigen_symmetric
from spectral_clustering_visualizer.metrics import cluster_size_map, result_summary
from spectral_clustering_visualizer.spectral import spectral_clustering


def test_dataset_names_include_expected_values():
    names = dataset_names()

    assert "moons" in names
    assert "rings" in names
    assert "blobs" in names
    assert "bridge" in names
    assert "islands" in names
    assert "spiral" in names


def test_gaussian_affinity_is_symmetric():
    data = [[0.0, 0.0], [0.2, 0.0], [2.0, 2.0]]
    affinity = gaussian_affinity(data, sigma=0.5)

    assert len(affinity) == 3
    assert affinity[0][1] == affinity[1][0]
    assert affinity[0][1] > affinity[0][2]


def test_knn_sparsification_preserves_shape():
    data = [[0.0, 0.0], [0.2, 0.0], [2.0, 2.0], [2.1, 2.0]]
    affinity = gaussian_affinity(data, sigma=0.5)
    sparse = sparsify_knn(affinity, k_neighbors=1)

    assert len(sparse) == 4
    assert len(sparse[0]) == 4
    assert any(value > 0 for row in sparse for value in row)


def test_normalized_laplacian_shape():
    data = [[0.0, 0.0], [0.2, 0.0], [2.0, 2.0]]
    affinity = gaussian_affinity(data, sigma=0.7)
    laplacian = normalized_laplacian(affinity)

    assert len(laplacian) == 3
    assert len(laplacian[0]) == 3
    assert abs(laplacian[0][0] - 1.0) < 1e-9


def test_jacobi_eigen_symmetric_simple_matrix():
    values, vectors = jacobi_eigen_symmetric([[2.0, 0.0], [0.0, 5.0]])

    assert values[0] <= values[1]
    assert abs(values[0] - 2.0) < 1e-6
    assert abs(values[1] - 5.0) < 1e-6
    assert len(vectors) == 2


def test_kmeans_basic_groups():
    data = [[0.0, 0.0], [0.1, 0.0], [3.0, 3.0], [3.1, 3.0]]
    labels, centers = kmeans(data, k=2, seed=1)

    assert len(labels) == 4
    assert len(centers) == 2
    assert len(set(labels)) == 2


def test_spectral_clustering_on_blobs():
    data = generate_dataset("blobs", seed=42)
    result = spectral_clustering(data, k=3, sigma=0.48, k_neighbors=10, seed=42)

    assert len(result.labels) == len(data)
    assert result.cluster_count >= 2
    assert result.embedding
    assert result.eigenvalues[0] <= result.eigenvalues[1]
    assert cluster_size_map(result.labels)


def test_result_summary_contains_expected_keys():
    data = generate_dataset("moons", seed=42)
    result = spectral_clustering(data, k=2, sigma=0.34, k_neighbors=10, seed=42)
    summary = result_summary(result)

    assert "cluster_count" in summary
    assert "cluster_sizes" in summary
    assert "first_eigenvalues" in summary
