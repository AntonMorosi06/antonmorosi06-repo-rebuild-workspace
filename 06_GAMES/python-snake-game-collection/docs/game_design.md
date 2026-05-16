# Game design

The project separates the Snake game into a shared core and multiple interfaces.

The core module owns the rules. It stores the grid size, snake body, direction, food position, score, step count and game-over state. It also handles direction changes, movement, collision checks and food placement.

The interface modules do not duplicate the rules. They render the current state and translate user input into calls to the core game.

This makes the collection easier to test. A bug in movement or scoring can be fixed once in the core instead of being fixed separately in curses, Tkinter and Pygame versions.
