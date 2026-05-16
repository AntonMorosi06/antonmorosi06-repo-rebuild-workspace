# MIDI pipeline

The project writes MIDI files directly with a small pure Python writer.

The composer creates symbolic note events. Each event has a track name, MIDI note number, start beat, duration, velocity and channel.

The MIDI writer converts beats into ticks using 480 ticks per beat. It then creates note-on and note-off events, stores them into separate tracks and writes a standard MIDI file.

The generated tracks are melody, bass, chords, pad and drums.

The drums use MIDI channel 10, represented internally as channel 9 because MIDI channels are zero-indexed in code.
