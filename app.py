import streamlit as st
from config import settings
from core import get_ai_response, AIClientError, build_scene_prompt, ConversationManager, parse_script, main_character



if "conversation" not in st.session_state:
  st.session_state.conversation = ConversationManager(max_turns=settings.MAX_HISTORY_TURNS)
if "rehearse_count" not in st.session_state:
  st.session_state.rehearse_count = 0
if "current_line_idx" not in st.session_state:
  st.session_state.current_line_idx = 0


def clear_scene():
  st.session_state.conversation.turns = []
  st.session_state.current_line_idx = 0 

#ui-elements
st.title("AI Line Partner")

#file uploader
uploaded_file = st.file_uploader("Upload your script file (.txt)", type=["txt"])

parsed_lines = []
unique_characters = []

if uploaded_file is not None:
  raw_text = uploaded_file.read().decode("utf-8")

  parsed_lines = parse_script(raw_text)
  unique_characters = main_character(parsed_lines, min_lines=3)
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
  st.session_state.current_line_idx = 0 #reset pointer to start of script

  idx = 0
  scene_window = parsed_lines[idx : idx + 10] #next 10 lines of context
  st.session_state.conversation.system_prompt = build_scene_prompt(user_character, scene_window)
  
  st.success("Script loaded! Ready to rehearse")

st.divider()

#recalculates and stays visible on screen every time the UI re-renders!
idx = st.session_state.current_line_idx

#check to make sure we didn't reach the end
if parsed_lines and idx < len(parsed_lines):
  upcoming = parsed_lines[idx]
  if upcoming.character == user_character:
    if st.button("Show my line"):
      st.caption(f"Your line : {upcoming.dialogue}")
    else:
      st.caption(f"Scene continues. {upcoming.character} speaks next.")
      
next_line = st.text_input("Enter your next line:", key="next_line_input")


rehearse_disabled = uploaded_file is None or not user_character or not next_line.strip()
if st.button("Rehearse", disabled=rehearse_disabled):
  convo = st.session_state.conversation

 # Check to make sure we didn't reach the end
  if parsed_lines and idx < len(parsed_lines):
    # log user turn
    convo.add_actor_line(next_line)
    st.session_state.current_line_idx += 1 
 
    #log AI turn
    next_idx = st.session_state.current_line_idx
    if next_idx < len(parsed_lines):
      partner_line = parsed_lines[next_idx]

      if partner_line.character != user_character:
        try:
          answer = get_ai_response(convo.to_messages())
        except AIClientError as e:
          st.error(f"Error talking to AI: {e}")
        else:
          convo.add_ai_line(answer)
          st.session_state.current_line_idx += 1
          st.rerun() #instant refresh and show next cue
  else: 
    st.info("You've reached the end of the script!")



## will implement this for improv mode 
#character = st.text_input("Enter your scene partner's character: ",key='scene_partner')
#context = st.text_area("Enter the context of the scene(up to 3-5 sentences): ",key='context')
#line = st.text_input("Enter your line: ",key='line')



#clear chat button
st.button("Clear Scene", on_click=clear_scene)

#responses space
st.divider()
for turn in st.session_state.conversation.turns:
  speaker = "You" if turn["role"] == "user" else "Partner"
  st.write(f"**{speaker}**: {turn['content']}")








