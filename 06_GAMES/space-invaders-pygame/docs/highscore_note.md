# High score note

The game stores a local high score in:

data/highscore.json

This file is ignored by git because it is runtime user data.

The helper loads a missing file as zero, saves a JSON object and updates the value only when the current score is higher.

Future versions can add player initials, score history, difficulty names and timestamps.
