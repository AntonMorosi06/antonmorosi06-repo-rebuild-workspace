# Markov model

The melody generator uses a simple Markov-inspired transition model over scale degrees.

A scale degree is not a fixed MIDI note. It is a position inside the selected scale. This makes the melody generator reusable across different keys and modes.

The transition model prefers small melodic movements. Staying on the same degree is possible, moving by one or two degrees is common, and larger jumps are less common. Stable degrees receive a small weight bonus.

This is not a trained neural model. It is a transparent educational generator. The advantage is that the output is easy to explain and debug.
