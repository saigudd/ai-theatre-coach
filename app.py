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
  st.session_state.conversation.system_prompt = ""
  st.session_state.current_line_idx = 0 

#ui-elements
st.set_page_config(page_title="AI Theatre Coach", page_icon="🎭")

#file uploader
uploaded_file = st.file_uploader("Upload your script file (.txt)", type=["txt"])

parsed_lines = []
unique_characters = []

if uploaded_file is not None:
  raw_text = uploaded_file.read().decode("utf-8")
  parsed_lines = parse_script(raw_text)
  unique_characters = main_character(parsed_lines, min_lines=3)

  parsed_lines = [line for line in parsed_lines if line.character in unique_characters]


  if not unique_characters:
    st.warning("No characters detected. This parser expects standard screenplay formatting (ALL CAPS name on its own line.")

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

##showcasing the rehearsal

with st.form(key="rehearse_form", clear_on_submit=True):
  next_line = st.text_input("Enter your next line:")
  submitted = st.form_submit_button(
    "Rehearse", disabled=(uploaded_file is None or not user_character)
  )   

if submitted:
  if not next_line.strip():
    st.warning("Type a line first.")
  elif idx >= len(parsed_lines):
    st.info("You've reached the end of the script!")
  else: 
    convo = st.session_state.conversation
    convo.add_actor_line(user_character, next_line)
    st.session_state.current_line_idx += 1

    next_idx = st.session_state.current_line_idx
    ai_should_respond = (
      next_idx < len(parsed_lines)
      and parsed_lines[next_idx].character != user_character
    )

    if ai_should_respond:
      try:
        with st.spinner("Partner is thinking..."):

          upcoming_character = parsed_lines[next_idx].character 
          scene_window = parsed_lines[idx : idx + 10] #ai constantly gets context, hence be able to switch character if needed

          convo.system_prompt = build_scene_prompt(
            user_character=user_character,
            ai_character=upcoming_character,
            upcoming_lines=scene_window
          )

          answer = get_ai_response(convo.to_messages())
      except AIClientError as e:
        st.error(f"Error talking to AI: {e}")
      else:
        convo.add_ai_line(upcoming_character, answer)
        st.session_state.current_line_idx += 1
        st.rerun()
    else:
      st.rerun() #runs twice so it stops this execution and start a fresh script from the top.


## will implement this for improv mode 
#character = st.text_input("Enter your scene partner's character: ",key='scene_partner')
#context = st.text_area("Enter the context of the scene(up to 3-5 sentences): ",key='context')
#line = st.text_input("Enter your line: ",key='line')



#clear chat button
st.button("Clear Scene", on_click=clear_scene)

#responses space
st.divider()
for turn in st.session_state.conversation.turns:
  #shows the user_character instead of "YOU"
  speaker = turn.get('character', 'You' if turn["role"] == "user" else "Partner")
  st.write(f"**{speaker}**: {turn['content']}")








