


def build_scene_prompt(user_character: str, ai_character: str, upcoming_lines: list) -> str:
  scene_excerpt = "\n".join(
    f"{line.character}: {line.dialogue}" for line in upcoming_lines)
  
  return f"""You are helping an actor rehearse a scene from a script.
  
  The actor is playing {user_character}.
  You are currently playing the role of {ai_character} in this scene.

  Here is the upcoming portion of the script, for reference on tone,
  plot, and what the other character(s) originally said:
  {scene_excerpt}

  The actor may paraphrase or improvise rather than reciting the script
  exactly, so react naturally in character as {ai_character} to  whatever they actually say,
  using the script excerpt above as your guide to the scene's content
  and direction, not as a rigid transcript to repeat verbatim. 
  If the scene switches to different setting, adapt {ai_character} accordingly.
  Respond only with dialogue, no stage directions, no explanations.
  Keep responses brief (1-3 sentences)."""