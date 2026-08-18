import streamlit as st
from config import settings
from core import get_ai_response, AIClientError, build_sys_prompt, ConversationManager, parse_script
from openai import OpenAI
from dotenv import load_dotenv


if "conversation" not in st.session_state:
  st.session_state.conversation = ConversationManager(max_turns=settings.MAX_HISTORY_TURNS)
if "rehearse_count" not in st.session_state:
  st.session_state.rehearse_count = 0

def clear_scene():
  st.session_state.conversation.turns = []
  

#ui-elements
st.title("AI Line Partner")


uploaded_file = st.file_uploader("Upload your script file (.txt)", type=["txt"])

parsed_lines = []
unique_characters = []

if uploaded_file is not None:
  raw_test = uploaded_file.read().decode("utf-8")
  parsed_lines = parse_script(raw_test)
  unique_characters = sorted(list(set(line.character for line in parsed_lines)))

#dropdown for user to pick character
user_character = st.selectbox(
  "Select the character YOU are playing!:",
  options=unique_characters,
  disabled=(uploaded_file is None) #will not show until file is uploaded
)

for line in parsed_lines:
  convo = ConversationManager()
  if line.character == user_character:
    convo.add_actor_line(line.dialogue)
  else:
    convo.add_ai_line(line.dialogue)

## will implement this for improv mode 
#character = st.text_input("Enter your scene partner's character: ",key='scene_partner')
#context = st.text_area("Enter the context of the scene(up to 3-5 sentences): ",key='context')
#line = st.text_input("Enter your line: ",key='line')


#rehearse button 
#TODO: rewire the rehease button to step through script
st.info("Upload a script and pick your role. Activating rehearsal logic (tomorrow)")


#clear chat button
st.button("Clear Scene", on_click=clear_scene)

#responses space
st.divider()
for turn in st.session_state.conversation.turns:
  speaker = "You" if turn["role"] == "user" else "Partner"
  st.write(f"**{speaker}: {turn['content']}")








