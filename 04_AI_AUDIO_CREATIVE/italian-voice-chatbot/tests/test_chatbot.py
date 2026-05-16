from italian_voice_chatbot.chatbot import ChatBot
from italian_voice_chatbot.intents import classify_intent
from italian_voice_chatbot.text_utils import normalize_text, is_exit_command


def test_normalize_text_removes_case_and_extra_spaces():
    assert normalize_text("  CIAO!!!   ") == "ciao"


def test_exit_command_detection():
    assert is_exit_command("esci")
    assert is_exit_command("quit")
    assert not is_exit_command("microbot")


def test_microbot_intent_is_detected():
    intent = classify_intent("parlami del progetto MicroBot e della telemetria")

    assert intent is not None
    assert intent.name == "microbot"


def test_chatbot_reply_adds_history():
    bot = ChatBot()
    response = bot.reply("ciao")

    assert response
    assert len(bot.history) == 2
    assert bot.history[0].role == "user"
    assert bot.history[1].role == "assistant"


def test_transcript_contains_messages():
    bot = ChatBot()
    bot.reply("chi sei")
    transcript = bot.transcript_text()

    assert "user:" in transcript
    assert "assistant:" in transcript
