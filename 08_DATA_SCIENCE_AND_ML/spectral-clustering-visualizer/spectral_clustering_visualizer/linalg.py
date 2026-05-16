from __future__ import annotations

import math


Vector = list[float]
Matrix = list[list[float]]


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def distance(a: Vector, b: Vector) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def norm(vector: Vector) -> float:
    return math.sqrt(dot(vector, vector))


def normalize(vector: Vector) -> Vector:
    value = norm(vector)
    if value < 1e-12:
        return vector[:]
    return [x / value for x in vector]


def row_normalize(matrix: Matrix) -> Matrix:
    return [normalize(row) for row in matrix]


def transpose(matrix: Matrix) -> Matrix:
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]


def identity(size: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]


def jacobi_eigen_symmetric(matrix: Matrix, max_iterations: int = 220, tolerance: float = 1e-9) -> tuple[Vector, Matrix]:
    n = len(matrix)
    if n == 0:
        raise ValueError("matrix cannot be empty")
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix must be square")

    a = [row[:] for row in matrix]
    v = identity(n)

    if n == 1:
        return [a[0][0]], [[1.0]]

    for _ in range(max_iterations):
        p = 0
        q = 1
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
            angle = math.pi / 4.0
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

    eigenvalues = [float(a[i][i]) for i in range(n)]
    eigenvectors = transpose(v)

    pairs = sorted(zip(eigenvalues, eigenvectors), key=lambda item: item[0])
    sorted_values = [value for value, _ in pairs]
    sorted_vectors = [normalize(vector) for _, vector in pairs]

    return sorted_values, sorted_vectors
