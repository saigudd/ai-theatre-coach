from core.conversation import ConversationManager

def test_add_actor_line_appends_user_role():
  convo = ConversationManager()
  convo.add_actor_line("HAMLET", "To be or not to be?")
  assert convo.turns[0] == {"role": "user", "content":"To be or not to be?","character":"HAMLET"}

def test_add_ai_line_appends_assistant_role():
  convo = ConversationManager()
  convo.add_ai_line("GHOST","A question worth asking.")
  assert convo.turns[0] == {"role": "assistant", "content": "A question worth asking.","character":"GHOST"}

def test_to_messages_puts_system_prompt_first():
  convo = ConversationManager(system_prompt="Bye.")
  convo.add_actor_line("HAMLET","Hello")
  messages = convo.to_messages()
  assert messages[1] == {"role": "user", "content":"Hello"}
  assert len(messages) == 2

def test_to_messages_with_no_turns():
  convo = ConversationManager(system_prompt="Be Hamlet.")
  messages = convo.to_messages()
  assert len(messages) == 1
  assert messages[0] == {"role": "system", "content": "Be Hamlet."}

def test_to_messages_trims_when_over_max_turns():
  convo = ConversationManager(system_prompt="sys", max_turns=1)
  for i in range(5):
    convo.add_actor_line("HAMLET", f"line {i}")
    convo.add_ai_line("GHOST",  f"reply {i}")
  messages = convo.to_messages()

  assert len(messages) == 3
  assert messages[0] == {"role": "system", "content": "sys"}
  assert messages[1] == {"role": "user", "content": "line 4"}
  assert messages[2] == {"role": "assistant", "content": "reply 4"}

def test_to_messages_with_max_turns_zero():
  convo = ConversationManager(system_prompt="sys", max_turns=0)
  convo.add_actor_line("HAMLET", "line 1")
  convo.add_ai_line("GHOST","reply 1")
  convo.add_actor_line("HAMLET", "line 2")
  messages = convo.to_messages()

  #intially thought it would be 0, but 0: means to provide ALL of the dict
  assert len(messages) == 1
  assert messages[0] == {"role": "system", "content": "sys"}
 