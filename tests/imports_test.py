import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("module", [
    "core.script_parser", "core.conversation", "core.prompts",
    "core.ai_client", "tests.openai_test",
])
def test_import_needs_neither_configuration_nor_client(module):
    # Fresh processes prevent Python's module cache from hiding import side effects.
    code = """
import importlib, sys
from unittest.mock import patch
with patch('openai.OpenAI', side_effect=AssertionError('Client created at import')):
    importlib.import_module(sys.argv[1])
assert 'config' not in sys.modules, 'Import loaded application configuration'
assert 'streamlit' not in sys.modules, 'Import loaded the UI framework'
"""
    result = subprocess.run(
        [sys.executable, "-B", "-c", code, module], cwd=ROOT,
        env=os.environ.copy(), capture_output=True, text=True, timeout=45,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_default_collection_is_safe_without_credentials():
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "--collect-only", "-q",
         "-p", "no:cacheprovider"], cwd=ROOT,
        env=os.environ.copy(), capture_output=True, text=True, timeout=45,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "tests collected" in result.stdout
