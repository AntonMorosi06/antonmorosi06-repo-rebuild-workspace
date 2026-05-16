# Game design

The project separates core gameplay from rendering.

The core module contains player state, alien state, bullet state, movement, collision detection, wave spawning, scoring, lives and level progression.

The Pygame layer handles keyboard input, drawing, timing, pause/reset behavior and high score display.

This separation makes the game easier to test. Collision rules and scoring can be checked without opening a graphical window.
