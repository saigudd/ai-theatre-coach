import os
from openai import OpenAI, OpenAIError
from config import settings
import streamlit as st

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class AIClientError(Exception):
  "raised when AI client fails to return a response"

def get_ai_response(messages: list[dict]) -> str:
  try:
    response = client.responses.create(
      model=settings.MODEL,
      input=messages
    )
  except OpenAIError as e:
    raise AIClientError(f"AI request failed: {e}") from e

  if not response.output_text:
    raise AIClientError("AI returned an empty response.")

  return response.output_text


