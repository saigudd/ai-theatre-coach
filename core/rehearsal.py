from dataclasses import dataclass
from hashlib import sha256
from typing import Sequence

from .conversation import ConversationManager
from .script_parser import ScriptLine


def script_fingerprint(raw_text: str) -> str:
  """Identify script contents even when two uploads have the same filename."""
  return sha256(raw_text.encode("utf-8")).hexdigest()


@dataclass
class RehearsalSession:
  script_id: str
  script_name: str
  actor: str
  lines: tuple[ScriptLine, ...]
  current_line_idx: int
  conversation: ConversationManager
  last_error: str | None = None

  @classmethod
  def start(
    cls,
    *,
    raw_text: str,
    script_name: str,
    lines: Sequence[ScriptLine],
    actor: str,
    max_history_turns: int,
  ) -> "RehearsalSession":
    """Create a fresh session bound to one script and one actor."""
    session_lines = tuple(lines)
    starting_idx = next(
      (index for index, line in enumerate(session_lines) if line.character == actor),
      None,
    )
    if starting_idx is None:
      raise ValueError(f"Actor {actor!r} has no dialogue in this script.")

    return cls(
      script_id=script_fingerprint(raw_text),
      script_name=script_name,
      actor=actor,
      lines=session_lines,
      current_line_idx=starting_idx,
      conversation=ConversationManager(max_turns=max_history_turns),
    )

  def restart(self) -> "RehearsalSession":
    """Restart the same script/actor with fresh rehearsal-specific state."""
    starting_idx = next(
      index for index, line in enumerate(self.lines) if line.character == self.actor
    )
    return type(self)(
      script_id=self.script_id,
      script_name=self.script_name,
      actor=self.actor,
      lines=self.lines,
      current_line_idx=starting_idx,
      conversation=ConversationManager(max_turns=self.conversation.max_turns),
    )
