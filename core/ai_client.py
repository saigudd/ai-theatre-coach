from functools import lru_cache

from openai import OpenAI, OpenAIError

class AIClientError(Exception):
  "raised when AI client fails to return a response"

@lru_cache(maxsize=1)
def _get_client() -> OpenAI:
  """Create the shared client on first use, not when a module is imported."""
  from config import settings

  if not settings.OPENAI_API_KEY:
    raise AIClientError("OPENAI_API_KEY is not configured.")
  return OpenAI(api_key=settings.OPENAI_API_KEY)


def get_ai_response(
  messages: list[dict], *, client: OpenAI | None = None, model: str | None = None
) -> str:
  """Generate dialogue; callers may supply a client/model for offline testing."""
  if model is None:
    from config import settings
    model = settings.MODEL

  try:
    active_client = client if client is not None else _get_client()
    response = active_client.responses.create(
      model=model,
      input=messages
    )
  except OpenAIError as e:
    raise AIClientError(f"AI request failed: {e}") from e

  if not response.output_text:
    raise AIClientError("AI returned an empty response.")

  return response.output_text


