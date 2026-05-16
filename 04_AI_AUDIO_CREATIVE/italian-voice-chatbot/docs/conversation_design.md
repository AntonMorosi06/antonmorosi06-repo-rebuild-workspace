# Conversation design

This chatbot is rule-based. It does not generate open-ended answers from a large neural model. It normalizes the user message, checks whether specific keywords are present and selects a response from the best matching intent.

The current intents cover greeting, identity, MicroBot, study, motivation, help, privacy, thanks and goodbye.

This design is intentionally simple. It is useful for learning how conversational structure works before introducing heavier machine learning or API-based models.

Future improvements could include intent confidence scores, YAML intent files, user profile memory, GUI mode, local speech recognition, wake-word detection and MicroBot dashboard commands.
