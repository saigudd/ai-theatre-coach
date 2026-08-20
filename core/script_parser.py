from dataclasses import dataclass
from collections import Counter

@dataclass
class ScriptLine:
  character: str
  dialogue: str
  stage_direction: str | None = None

def parse_script(raw_test: str) -> list[ScriptLine]:
  """v1: replace with LLM parsing later if real scripts dont fit the format"""

  result = []
  current_character = None
  dialogue_buffer = []

  def flush():

    #these belong to outer function scope
    nonlocal current_character, dialogue_buffer
    if current_character is not None and len(dialogue_buffer) >= 1:
      
      
      fdialogue = " ".join(dialogue_buffer)
      rdialogue = ScriptLine(character=current_character, dialogue=fdialogue)
      result.append(rdialogue)

      #resets for next character/dialogue
      current_character = None
      dialogue_buffer = []
      pass

  for raw_line in raw_test.splitlines():
    line = raw_line.strip()

    if is_character_line(line):
      flush()
      current_character = line
      continue

    if line.startswith("(") and line.endswith(")"):
      continue

    if line == "":
      flush()
      continue 

    if current_character is not None:
      dialogue_buffer.append(line)

  flush()
  return result


def is_character_line(line: str) -> bool:
  stripped = line.strip()

  if not stripped:
    return False

  if not stripped.isupper():
    return False

  if len(stripped) > 40:
    return False

  if stripped.startswith("(") and stripped.endswith(")"):
    return False

  scene_prefixes = (
    "INT.",
    "EXT.",
    "INT./EXT.",
    "EXT./INT.",
    "CUT TO:",
    "FADE OUT."
)

  if stripped.startswith(scene_prefixes):
    return False

  suspicious_char = ("!","?",",",".","--")

  if any(ch in stripped for ch in suspicious_char):
    return False

  if stripped.endswith(":"):
    return False  

  return True 


def main_character(lines: list[ScriptLine], min_lines: int = 3) -> list[str]:
  """filters out junk(headings, sound effects,
  by keeping names that speak at least 'min_lines' times"""\

  count = Counter(line.character for line in lines)

  frequent_characters = [name for name, count in count.items() if count >= min_lines]

  return sorted(frequent_characters)
  pass