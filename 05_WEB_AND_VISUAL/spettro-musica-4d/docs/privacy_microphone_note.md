# Microphone privacy note

The default mode is synthetic and does not use the microphone.

Microphone access starts only when the user clicks Start microphone and accepts the browser permission request.

The app uses the Web Audio API analyser node to compute frequency-domain values in the browser. This reconstructed baseline does not intentionally upload microphone audio to a server.

Users should still avoid testing with private conversations, sensitive environments or personal information. Browser behavior and permissions should always be checked before public demos.

For GitHub Pages deployment, microphone access generally requires HTTPS, which GitHub Pages provides.
