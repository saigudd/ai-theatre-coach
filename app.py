import streamlit as st
from config import settings
from core.ai_client import get_ai_response, AIClientError
from core.prompts import build_sys_prompt
from core.conversation import ConversationManager
from openai import OpenAI
from dotenv import load_dotenv

if "conversation" not in st.session_state:
  st.session_state.conversation = ConversationManager(max_turns=settings.MAX_HISTORY_TURNS)
if "rehearse_count" not in st.session_state:
  st.session_state.rehearse_count = 0

def clear_scene():
  st.session_state.conversation.turns = []
  st.session_state.line = ""
  st.session_state.scene_partner = ""
  st.session_state.context = ""
  

#ui-elements
st.title("AI Line Partner")

character = st.text_input("Enter your scene partner's character: ",key='scene_partner')
context = st.text_area("Enter the context of the scene(up to 3-5 sentences): ",key='context')
line = st.text_input("Enter your line: ",key='line')


#rehearse button 
if st.button("Rehearse"):

  convo = st.session_state.conversation
  convo.system_prompt = build_sys_prompt(character, context)
  convo.add_actor_line(line)

  try:
    answer = get_ai_response(convo.to_messages())
  except AIClientError as e:
    st.error(f"Something went wrong talking to AI: {e}")
  else:
    convo.add_ai_line(answer)
    st.session_state.rehearse_count += 1

  
#clear chat button
st.button("Clear Scene", on_click=clear_scene)

#responses space
st.divider()
for turn in st.session_state.conversation.turns:
  speaker = "You" if turn["role"] == "user" else (character or "AI")
  st.write(f"**{speaker}: {turn['content']}")








