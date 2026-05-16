# Privacy note

The core project does not require real personal data. It uses synthetic data.

Do not send real personal profiles, real salaries, private employment information or identifying data to this API during demos.

The optional TTS helper can use gTTS, which may contact an external service to generate speech. Avoid private content in TTS tests.

The repository includes an .env.example file, but no secret key should be committed. If future versions integrate external LLM APIs, API keys must stay in local environment variables and must not be published.
