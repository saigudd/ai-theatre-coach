import os
from dotenv import load_dotenv

load_dotenv()

class settings:
  MODEL = os.getenv("THEATRE_COACH_MODEL", "gpt-4o-mini")
  MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_LINES", "6"))

  