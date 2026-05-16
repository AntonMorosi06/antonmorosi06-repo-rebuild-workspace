# Performance notes

The implementation is educational and uses dense matrices.

The Gaussian affinity computation is O(n²).

The Jacobi eigen decomposition is suitable only for relatively small datasets in this reconstructed baseline.

For production-scale spectral clustering, optimized numerical libraries and sparse eigen solvers should be used.

The current visualizer intentionally keeps dataset sizes moderate so that the whole pipeline remains inspectable and runnable as a portfolio demo.
