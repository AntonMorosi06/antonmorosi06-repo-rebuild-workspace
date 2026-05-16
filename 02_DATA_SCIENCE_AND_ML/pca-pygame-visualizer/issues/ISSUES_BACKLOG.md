# Issues Backlog for pca-pygame-visualizer

## Issue 01: Validate local run

Goal:
Confirm the app opens and runs.

Tasks:
- [ ] Create virtual environment.
- [ ] Install requirements.
- [ ] Run python src/pca_demo_pygame.py.
- [ ] Confirm window opens.

Acceptance criteria:
- Application runs without crash.

## Issue 02: Add screenshot evidence

Goal:
Create portfolio evidence.

Tasks:
- [ ] Run the app.
- [ ] Press S to save screenshot.
- [ ] Copy best screenshot into demos/screenshots.
- [ ] Update README if needed.

Acceptance criteria:
- Screenshot exists under demos/screenshots.

## Issue 03: Add optional CSV import

Goal:
Allow the visualizer to load real 3D numeric data.

Tasks:
- [ ] Add argparse.
- [ ] Support CSV with three numeric columns.
- [ ] Document expected format.

Acceptance criteria:
- Synthetic mode and CSV mode both work.

## Issue 04: Add tests for PCA calculation

Goal:
Validate PCA computation.

Tasks:
- [ ] Add pytest.
- [ ] Test eigenvalue ordering.
- [ ] Test explained variance sums to approximately one.

Acceptance criteria:
- Tests pass.

## Issue 05: Improve visual polish

Goal:
Make the app more portfolio-ready.

Tasks:
- [ ] Add smoother camera.
- [ ] Add optional trails or point glow.
- [ ] Add axis labels with better positioning.
- [ ] Add title animation.

Acceptance criteria:
- Visual quality improves without reducing clarity.
