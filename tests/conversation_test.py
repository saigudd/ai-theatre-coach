from core.conversation import ConversationManager

def test_to_messages_inclues_sys_and_history():
  convo = ConversationManager(system_prompt="Be Hamlet", max_turns=2)
  convo.add_actor_line("To be or not to be?")
  convo.add_ai_line("A question worth asking.")

  message = convo.to_messages()

  #message[0] = sys_promp, message[1] = actor, message[-1]  = ai
  assert message[0] == {"role": "system", "content": "Be Hamlet"}
  assert message[-1]['content'] == 'A question worth asking.'

def test_to_messages_trims_to_max_turns():
  convo = ConversationManager(system_prompt="sys", max_turns=1)
  for i in range(5):
    convo.add_actor_line(f"line {i}")
    convo.add_ai_line(f"line {i}")

  messages = convo.to_messages()
  assert len(messages) == 3