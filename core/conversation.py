from dataclasses import dataclass, field


@dataclass
class ConversationManager:
  system_prompt: str = ""
  turns: list[dict] = field(default_factory=list)
  max_turns: int = 6

  def add_actor_line(self, character_name: str, line: str):
    self.turns.append({"role": "user", "content": line, "character": character_name})

  def add_ai_line(self, character_name: str, line: str):
    self.turns.append({"role": "assistant", "content": line, "character": character_name})

  def to_messages(self) -> list[dict]:
    if self.max_turns == 0: 
      return [{"role": "system", "content": self.system_prompt}]
    history = self.turns[-(self.max_turns * 2):]

    #ensures API gets only "role" and "content"
    cleaned_history = [{"role": turn['role'], "content": turn["content"]} for turn in history]

    return [{"role": "system", "content": self.system_prompt}] + cleaned_history
