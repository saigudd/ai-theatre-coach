import streamlit as st
from config import settings
from core import get_ai_response, AIClientError, build_sys_prompt, ConversationManager, parse_script
from dotenv import dotenv_values


if "conversation" not in st.session_state:
  st.session_state.conversation = ConversationManager(max_turns=settings.MAX_HISTORY_TURNS)
if "rehearse_count" not in st.session_state:
  st.session_state.rehearse_count = 0


def clear_scene():
  st.session_state.conversation.turns = []

#ui-elements
st.title("AI Line Partner")

#file uploader
uploaded_file = st.file_uploader("Upload your script file (.txt)", type=["txt"])

parsed_lines = []
unique_characters = []

if uploaded_file is not None:
  raw_text = uploaded_file.read().decode("utf-8")

  
  st.write("Characters around the beginning of the file:")
  st.text(raw_text[:3000])

  st.write("Characters around the middle of the file:")
  middle = len(raw_text) // 2
  st.text(raw_text[middle:middle + 5000])

  #parsed_lines = parse_script(raw_text)
  #unique_characters = sorted(list(set(line.character for line in parsed_lines)))
else:
  parsed_lines = []
  unique_characters = []

#dropdown for user to pick character
user_character = st.selectbox(
  "Select the character YOU are playing!:",
  options=unique_characters,
  disabled=(uploaded_file is None) #will not show until file is uploaded
)

load_disabled = uploaded_file is None or not user_character
if st.button("Load Script ", disabled=load_disabled):
  st.session_state.conversation.turns = [] #wipes previous scenes
  st.session_state.conversation.system_prompt = build_sys_prompt(user_character)
  for line in parsed_lines:
    if line.character == user_character:
      st.session_state.conversation.add_actor_line(line.dialogue)
    else:
      st.session_state.conversation.add_ai_line(line.dialogue)

next_line = st.text_input("Enter your next line:", key="next_line_input")

rehearse_disabled = uploaded_file is None or not user_character or not next_line.strip()
if st.button("Rehearse", disabled=rehearse_disabled):
  convo = st.session_state.conversation
  convo.add_actor_line(next_line)
  try:
    answer = get_ai_response(convo.to_messages())
  except AIClientError as e:
    st.error(f"Error talking to AI: {e}")
  else:
    convo.add_ai_line(answer)



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
  st.write(f"**{speaker}**: {turn['content']}")








