from types import SimpleNamespace
from unittest.mock import Mock

from openai import OpenAIError
import pytest

from core import ai_client


def test_injected_client_receives_messages_and_model():
    client = Mock()
    client.responses.create.return_value = SimpleNamespace(output_text="Hello.")
    messages = [{"role": "user", "content": "Your cue."}]

    assert ai_client.get_ai_response(messages, client=client, model="test-model") == "Hello."
    client.responses.create.assert_called_once_with(model="test-model", input=messages)


def test_empty_output_is_an_application_error():
    client = Mock()
    client.responses.create.return_value = SimpleNamespace(output_text="")

    with pytest.raises(ai_client.AIClientError, match="empty response"):
        ai_client.get_ai_response([], client=client, model="test-model")


def test_provider_error_preserves_its_cause():
    client = Mock()
    failure = OpenAIError("Simulated provider failure")
    client.responses.create.side_effect = failure

    with pytest.raises(ai_client.AIClientError, match="AI request failed") as caught:
        ai_client.get_ai_response([], client=client, model="test-model")
    assert caught.value.__cause__ is failure


@pytest.fixture
def default_client(monkeypatch):
    from config import settings

    monkeypatch.setattr(settings, "OPENAI_API_KEY", None)
    ai_client._get_client.cache_clear()
    constructor = Mock()
    constructor.return_value.responses.create.return_value = SimpleNamespace(output_text="Hello.")
    monkeypatch.setattr(ai_client, "OpenAI", constructor)
    yield settings, constructor
    ai_client._get_client.cache_clear()


def test_missing_key_fails_only_when_requesting_ai(default_client):
    _, constructor = default_client
    with pytest.raises(ai_client.AIClientError, match="OPENAI_API_KEY"):
        ai_client.get_ai_response([])
    constructor.assert_not_called()


def test_default_client_is_reused_after_first_request(default_client, monkeypatch):
    settings, constructor = default_client
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-key-not-real")
    monkeypatch.setattr(settings, "MODEL", "configured-model")
    constructor.assert_not_called()

    assert ai_client.get_ai_response([]) == "Hello."
    assert ai_client.get_ai_response([]) == "Hello."
    constructor.assert_called_once_with(api_key="test-key-not-real")
    assert constructor.return_value.responses.create.call_count == 2
    constructor.return_value.responses.create.assert_called_with(model="configured-model", input=[])


def test_client_creation_error_is_wrapped(default_client, monkeypatch):
    settings, constructor = default_client
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-key-not-real")
    constructor.side_effect = OpenAIError("Simulated initialization failure")
    with pytest.raises(ai_client.AIClientError, match="AI request failed"):
        ai_client.get_ai_response([])
