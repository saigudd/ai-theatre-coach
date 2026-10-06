from config import settings
key = settings.OPENAI_API_KEY
print("Key loaded:", bool(key), "length:", len(key) if key else 0)
print("MODEL:", settings.MODEL)
print("MAX_HISTORY_TURNS:", settings.MAX_HISTORY_TURNS)