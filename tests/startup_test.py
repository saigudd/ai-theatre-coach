from pathlib import Path
from unittest.mock import Mock

from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"


def test_missing_key_shows_setup_message_without_starting_rehearsal(monkeypatch):
    from config import settings
    from core import ai_client

    monkeypatch.setattr(settings, "OPENAI_API_KEY", None)
    constructor = Mock(side_effect=AssertionError("Startup created an AI client"))
    monkeypatch.setattr(ai_client, "OpenAI", constructor)
    app = AppTest.from_file(str(APP), default_timeout=15).run()

    assert not app.exception
    assert any("OPENAI_API_KEY" in warning.value for warning in app.warning)
    assert not app.text_input
    constructor.assert_not_called()


def test_configured_startup_does_not_create_client(monkeypatch):
    from config import settings
    from core import ai_client

    monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-key-not-real")
    constructor = Mock(side_effect=AssertionError("Startup created an AI client"))
    monkeypatch.setattr(ai_client, "OpenAI", constructor)
    app = AppTest.from_file(str(APP), default_timeout=15).run()

    assert not app.exception
    assert app.title[0].value == "🎭 AI Theatre Coach 🎭"
    assert len(app.text_input) == 1
    constructor.assert_not_called()
