from dataclasses import dataclass, field

@dataclass
class ConversationManager:
  system_prompt: str = ""
  turns: list[dict] = field(default_factory=list)
  max_turns: int = 6

  def add_actor_line(self, line: str):
    self.turns.append({"role": "user", "content": line})

  def add_ai_line(self, line: str):
    self.turns.append({"role": "assistant", "content": line})

  def to_messages(self) -> list[dict]:
    if self.max_turns == 0: return {"role": "system", "content": self.system_prompt}
    history = self.turns[-(self.max_turns * 2): ]
    return [{"role": "system", "content": self.system_prompt}] + history
