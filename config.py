import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def _get_openai_api_key() -> str | None:
  """Read the API key from the environment, then Streamlit secrets."""
  api_key = os.getenv("OPENAI_API_KEY", "").strip()

  if not api_key:
    try:
      api_key = str(st.secrets.get("OPENAI_API_KEY", "")).strip()
    except (FileNotFoundError, KeyError):
      api_key = ""

  if api_key:
    # OpenAI() reads this variable when core.ai_client is imported.
    os.environ["OPENAI_API_KEY"] = api_key

  return api_key or None


class settings:
  OPENAI_API_KEY = _get_openai_api_key()
  MODEL = os.getenv("THEATRE_COACH_MODEL", "gpt-4o-mini")
  MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", "6"))

  
