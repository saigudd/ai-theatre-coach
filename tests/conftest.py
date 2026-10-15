"""Keep test collection and execution independent of local credentials/network."""

import socket

import pytest
import streamlit as st


_isolation = pytest.MonkeyPatch()


def _block_connection(*args, **kwargs):
    raise AssertionError("Network access is disabled in tests; use a fake client.")


def pytest_sessionstart(session):
    # Session hooks run before collection; fixtures alone cannot protect imports.
    _isolation.delenv("OPENAI_API_KEY", raising=False)
    _isolation.setenv("PYTHON_DOTENV_DISABLED", "1")
    _isolation.setenv("MAX_HISTORY_TURNS", "6")
    _isolation.setattr(st, "secrets", {})
    _isolation.setattr(socket.socket, "connect", _block_connection)
    _isolation.setattr(socket.socket, "connect_ex", _block_connection)
    _isolation.setattr(socket, "create_connection", _block_connection)


def pytest_sessionfinish(session, exitstatus):
    _isolation.undo()
