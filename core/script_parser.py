from dataclasses import dataclass

@dataclass
class ScriptLine:
  character: str
  dialogue: str

def parse_script(raw_test: str) -> list[ScriptLine]:
  """v1: replace with LLM parsing later if real scripts dont fit the format"""

  result = []

  for line in raw_test.splitlines():
    line = line.strip()
    if len(line) == 0:
      continue

    split = line.split(":", 1)
    if len(split) != 2:
      continue

    character = split[0].strip()
    dialogue = split[1].strip()
    new_line = ScriptLine(character, dialogue)
    result.append(new_line)
  
  return result 
      