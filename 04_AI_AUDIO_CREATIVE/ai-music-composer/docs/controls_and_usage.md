# Controls and usage

List styles:

python3 main.py styles

Generate a cinematic demo:

python3 main.py generate --style cinematic --seed 42 --name demo_cinematic

Generate an ambient demo:

python3 main.py generate --style ambient --seed 11 --name demo_ambient

Generate an arcade demo:

python3 main.py generate --style arcade --seed 7 --name demo_arcade

Generate a dark demo:

python3 main.py generate --style dark --seed 99 --name demo_dark

Each command creates a MIDI file, a WAV preview and a runtime Markdown report.
