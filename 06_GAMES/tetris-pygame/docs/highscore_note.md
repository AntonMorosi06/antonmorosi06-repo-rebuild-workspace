# High score note

The Pygame interface stores a local high score in:

data/highscore.json

This file is ignored by git because it is runtime user data.

The high score helper is intentionally small. It loads a missing file as zero, saves a JSON object and updates the score only when the new score is higher.

Future versions can add player names, timestamped score history or settings.
