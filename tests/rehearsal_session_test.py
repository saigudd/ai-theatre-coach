import io
from unittest.mock import Mock

import streamlit as st
from streamlit.testing.v1 import AppTest


SCRIPT_A = """INT. ROOM - DAY
BOB
Opening from script A.

ALICE
Alice line one.

BOB
Reply from script A.

ALICE
Alice line two.

BOB
Another reply from script A.

ALICE
Alice line three.
"""

SCRIPT_B = """INT. GARDEN - NIGHT
CAROL
Carol line one from script B.

DANA
Dana line one.

CAROL
Carol line two from script B.

DANA
Dana line two.

CAROL
Carol line three from script B.

DANA
Dana line three.
"""


class UploadedScript(io.BytesIO):
    def __init__(self, name: str, text: str):
        super().__init__(text.encode("utf-8"))
        self.name = name


def _button(app: AppTest, label: str):
    return next(button for button in app.button if button.label.strip() == label)


def test_loading_new_script_and_actor_isolates_rehearsal_state(monkeypatch):
    from config import settings
    import core

    selected_upload = {"name": "script_a.txt", "text": SCRIPT_A}

    def upload(*args, **kwargs):
        return UploadedScript(selected_upload["name"], selected_upload["text"])

    monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-key-not-real")
    monkeypatch.setattr(st, "file_uploader", upload)
    monkeypatch.setattr(core, "get_ai_response", Mock(return_value="Unused fake response"))

    app = AppTest.from_file("app.py", default_timeout=20).run()
    app.selectbox[0].select("ALICE").run()
    _button(app, "Start New Rehearsal").click().run()

    old_session = app.session_state.rehearsal
    old_session.conversation.add_actor_line("ALICE", "OLD SCRIPT A DIALOGUE")
    old_session.conversation.system_prompt = "OLD SCRIPT A PROMPT"
    old_session.current_line_idx = 4
    old_session.last_error = "OLD SCRIPT A ERROR"

    selected_upload.update(name="script_b.txt", text=SCRIPT_B)
    app.run()

    # Changing setup widgets is only a draft until the user starts a new rehearsal.
    assert app.session_state.rehearsal is old_session
    assert old_session.script_name == "script_a.txt"
    assert old_session.actor == "ALICE"
    assert old_session.current_line_idx == 4
    assert old_session.conversation.turns[0]["content"] == "OLD SCRIPT A DIALOGUE"

    app.selectbox[0].select("CAROL").run()
    _button(app, "Start New Rehearsal").click().run()

    new_session = app.session_state.rehearsal
    assert new_session.conversation.turns == []
    assert new_session.conversation.system_prompt == ""
    assert new_session.current_line_idx == 0
    assert new_session.last_error is None

    assert "rehearsal" in app.session_state
    assert new_session is not old_session
    assert new_session.script_name == "script_b.txt"
    assert new_session.actor == "CAROL"
    assert new_session.lines[new_session.current_line_idx].character == "CAROL"
    assert "script B" in new_session.lines[new_session.current_line_idx].dialogue

    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics == {
        "Screenplay": "script_b.txt",
        "Your role": "CAROL",
        "Current turn": "CAROL",
    }

    new_session.conversation.add_actor_line("CAROL", "OLD CAROL DIALOGUE")
    new_session.conversation.system_prompt = "OLD CAROL PROMPT"
    new_session.current_line_idx = 4
    new_session.last_error = "OLD CAROL ERROR"

    app.selectbox[0].select("DANA").run()
    assert app.session_state.rehearsal is new_session
    assert new_session.actor == "CAROL"
    _button(app, "Start New Rehearsal").click().run()

    dana_session = app.session_state.rehearsal
    assert dana_session is not new_session
    assert dana_session.script_id == new_session.script_id
    assert dana_session.actor == "DANA"
    assert dana_session.current_line_idx == 1
    assert dana_session.lines[dana_session.current_line_idx].character == "DANA"
    assert dana_session.conversation.turns == []
    assert dana_session.conversation.system_prompt == ""
    assert dana_session.last_error is None

    dana_session.current_line_idx = 5
    dana_session.conversation.add_actor_line("DANA", "OLD DANA DIALOGUE")
    dana_session.conversation.system_prompt = "OLD DANA PROMPT"
    dana_session.last_error = "OLD DANA ERROR"
    _button(app, "Restart Rehearsal").click().run()

    restarted_session = app.session_state.rehearsal
    assert restarted_session is not dana_session
    assert restarted_session.script_id == dana_session.script_id
    assert restarted_session.actor == "DANA"
    assert restarted_session.current_line_idx == 1
    assert restarted_session.conversation.turns == []
    assert restarted_session.conversation.system_prompt == ""
    assert restarted_session.last_error is None


def test_restart_preserves_identity_but_replaces_rehearsal_state():
    from core import RehearsalSession, parse_script

    original = RehearsalSession.start(
        raw_text=SCRIPT_B,
        script_name="script_b.txt",
        lines=parse_script(SCRIPT_B),
        actor="DANA",
        max_history_turns=3,
    )
    original.current_line_idx = 5
    original.conversation.add_actor_line("DANA", "OLD RESTART DIALOGUE")
    original.conversation.system_prompt = "OLD RESTART PROMPT"
    original.last_error = "OLD RESTART ERROR"

    restarted = original.restart()

    assert restarted is not original
    assert restarted.script_id == original.script_id
    assert restarted.script_name == "script_b.txt"
    assert restarted.actor == "DANA"
    assert restarted.lines == original.lines
    assert restarted.current_line_idx == 1
    assert restarted.conversation is not original.conversation
    assert restarted.conversation.max_turns == 3
    assert restarted.conversation.turns == []
    assert restarted.conversation.system_prompt == ""
    assert restarted.last_error is None
