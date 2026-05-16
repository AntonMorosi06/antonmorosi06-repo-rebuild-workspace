from pca_visualizer.datasets import dataset_names, generate_dataset
from pca_visualizer.linalg import covariance_matrix, jacobi_eigen_symmetric, mean_vector, center_data
from pca_visualizer.metrics import reconstruction_mse
from pca_visualizer.pca import fit_pca, transform


def test_dataset_names_include_expected_values():
    names = dataset_names()

    assert "correlated" in names
    assert "ellipse" in names
    assert "clusters" in names
    assert "ribbon3d" in names
    assert "line" in names


def test_mean_and_centering():
    data = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    mean = mean_vector(data)
    centered = center_data(data, mean)

    assert mean == [3.0, 4.0]
    assert abs(sum(row[0] for row in centered)) < 1e-9
    assert abs(sum(row[1] for row in centered)) < 1e-9


def test_covariance_matrix_shape():
    data = [[-1.0, -1.0], [0.0, 0.0], [1.0, 1.0]]
    cov = covariance_matrix(data)

    assert len(cov) == 2
    assert len(cov[0]) == 2
    assert cov[0][1] > 0


def test_jacobi_eigen_symmetric_diagonal_matrix():
    values, vectors = jacobi_eigen_symmetric([[3.0, 0.0], [0.0, 1.0]])

    assert values[0] >= values[1]
    assert abs(values[0] - 3.0) < 1e-6
    assert abs(values[1] - 1.0) < 1e-6
    assert len(vectors) == 2


def test_fit_pca_correlated_cloud():
    data = generate_dataset("correlated", seed=42)
    result = fit_pca(data, n_components=1)

    assert result.n_components == 1
    assert result.eigenvalues[0] >= result.eigenvalues[1]
    assert result.explained_variance_ratio[0] > 0.70
    assert len(result.transformed) == len(data)


def test_transform_new_points():
    data = generate_dataset("ellipse", seed=42)
    result = fit_pca(data, n_components=1)
    transformed = transform(data[:5], result)

    assert len(transformed) == 5
    assert len(transformed[0]) == 1


def test_reconstruction_error_decreases_with_more_components():
    data = generate_dataset("ribbon3d", seed=42)
    one = fit_pca(data, n_components=1)
    two = fit_pca(data, n_components=2)

    mse_one = reconstruction_mse(data, one.reconstructed)
    mse_two = reconstruction_mse(data, two.reconstructed)

    assert mse_two <= mse_one
