from __future__ import annotations

import math


Vector = list[float]
Matrix = list[list[float]]


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(vector: Vector) -> float:
    return math.sqrt(dot(vector, vector))


def subtract(a: Vector, b: Vector) -> Vector:
    return [x - y for x, y in zip(a, b)]


def add(a: Vector, b: Vector) -> Vector:
    return [x + y for x, y in zip(a, b)]


def scale(vector: Vector, scalar: float) -> Vector:
    return [x * scalar for x in vector]


def transpose(matrix: Matrix) -> Matrix:
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]


def mat_vec_mul(matrix: Matrix, vector: Vector) -> Vector:
    return [dot(row, vector) for row in matrix]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    b_t = transpose(b)
    return [[dot(row, col) for col in b_t] for row in a]


def identity(size: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]


def mean_vector(data: Matrix) -> Vector:
    if not data:
        raise ValueError("data cannot be empty")
    dimension = len(data[0])
    return [sum(row[index] for row in data) / len(data) for index in range(dimension)]


def center_data(data: Matrix, mean: Vector | None = None) -> Matrix:
    if not data:
        raise ValueError("data cannot be empty")
    mean = mean or mean_vector(data)
    return [subtract(row, mean) for row in data]


def covariance_matrix(centered: Matrix) -> Matrix:
    if not centered:
        raise ValueError("centered data cannot be empty")
    if len(centered) < 2:
        raise ValueError("at least two samples are required")

    dimension = len(centered[0])
    cov = [[0.0 for _ in range(dimension)] for _ in range(dimension)]

    for row in centered:
        for i in range(dimension):
            for j in range(dimension):
                cov[i][j] += row[i] * row[j]

    denom = len(centered) - 1
    return [[value / denom for value in line] for line in cov]


def jacobi_eigen_symmetric(matrix: Matrix, max_iterations: int = 120, tolerance: float = 1e-10) -> tuple[Vector, Matrix]:
    n = len(matrix)
    if n == 0:
        raise ValueError("matrix cannot be empty")
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix must be square")

    a = [row[:] for row in matrix]
    v = identity(n)

    for _ in range(max_iterations):
        p = 0
        q = 1 if n > 1 else 0
        max_off = 0.0

        for i in range(n):
            for j in range(i + 1, n):
                value = abs(a[i][j])
                if value > max_off:
                    max_off = value
                    p = i
                    q = j

        if max_off < tolerance:
            break

        if abs(a[p][p] - a[q][q]) < 1e-12:
            angle = math.pi / 4
        else:
            angle = 0.5 * math.atan2(2.0 * a[p][q], a[q][q] - a[p][p])

        c = math.cos(angle)
        s = math.sin(angle)

        for i in range(n):
            if i != p and i != q:
                aip = a[i][p]
                aiq = a[i][q]
                a[i][p] = c * aip - s * aiq
                a[p][i] = a[i][p]
                a[i][q] = s * aip + c * aiq
                a[q][i] = a[i][q]

        app = a[p][p]
        aqq = a[q][q]
        apq = a[p][q]

        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = 0.0
        a[q][p] = 0.0

        for i in range(n):
            vip = v[i][p]
            viq = v[i][q]
            v[i][p] = c * vip - s * viq
            v[i][q] = s * vip + c * viq

    eigenvalues = [a[i][i] for i in range(n)]
    eigenvectors = transpose(v)
    pairs = sorted(zip(eigenvalues, eigenvectors), key=lambda item: item[0], reverse=True)

    sorted_values = [float(value) for value, _ in pairs]
    sorted_vectors = [normalize_vector(vector) for _, vector in pairs]

    return sorted_values, sorted_vectors


def normalize_vector(vector: Vector) -> Vector:
    value = norm(vector)
    if value < 1e-12:
        return vector[:]
    return [x / value for x in vector]
