# Game design

The project separates the Tetris-style game into a pure Python core and a Pygame interface.

The core module owns board state, active piece, next queue, hold piece, collision detection, movement, rotation, lock, line clearing, score and level progression.

The Pygame interface owns rendering, keyboard input, timing, panel layout and high score display.

This separation makes the core testable without opening a graphical window. It also makes future interfaces easier to add.
