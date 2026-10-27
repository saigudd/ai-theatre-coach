import streamlit as st
from config import settings
from core import get_ai_response, AIClientError, build_scene_prompt, RehearsalSession, script_fingerprint, parse_script, main_character

#ui-elements
st.set_page_config(page_title="AI Theatre Coach", page_icon="🎭", layout="centered")
st.title("🎭 AI Theatre Coach 🎭")
st.caption("Upload a screenplay and rehearse opposite an AI partner who voices every other character.")

if not settings.OPENAI_API_KEY:
  st.warning(
    "The AI partner is not configured yet. The app owner needs to set "
    "OPENAI_API_KEY in the local .env file or Streamlit Secrets, then restart the app."
  )
  st.stop()

if "rehearsal" not in st.session_state:
  st.session_state.rehearsal = None


def restart_rehearsal():
  if st.session_state.rehearsal is not None:
    st.session_state.rehearsal = st.session_state.rehearsal.restart()

MAX_AI_TURNS_PER_CLICK = 4

def advance_through_other_characters(rehearsal, next_idx, max_turns):
  """Auto-generates AI dialogue for consecutive non-user characters.
  End parameters: user's next line, end of script, or max_turns (whichever comes first)
  WHY: to avoid unbounded, costly, off-script run."""
  
  turns_used = 0
  convo = rehearsal.conversation
  parsed_lines = rehearsal.lines
  user_character = rehearsal.actor
  
  while (
    next_idx < len(parsed_lines)
    and parsed_lines[next_idx].character != user_character
    and turns_used < max_turns
  ):
    ai_character = parsed_lines[next_idx].character
    scene_window = parsed_lines[next_idx : next_idx + 10]
    convo.system_prompt = build_scene_prompt(
      user_character=user_character,
      ai_character=ai_character,
      upcoming_lines=scene_window
    )
    try:
      with st.spinner(f"{ai_character} is thinking..."):
        answer = get_ai_response(convo.to_messages())
    except AIClientError as e:
      rehearsal.last_error = f"Error talking to AI: {e}"
      break #stops if API breaks
    else:
      convo.add_ai_line(ai_character, answer)
      next_idx += 1 #goes to the next line
      turns_used += 1
      
  return next_idx


#checks to see len(character's lines) and ends the rehearsal quickly IF len = small
SKIP_GAP_COUNT = 12

def next_user_line_idx(parsed_lines, start_idx, user_character):
  """idx of user's next line at/after start_idx, or None if they never speak again."""
  for i in range(start_idx, len(parsed_lines)):
    if parsed_lines[i].character == user_character:
      return i
  return None



#file 
with st.sidebar:
  st.subheader("Script")
  uploaded_file = st.file_uploader("Upload your script file (.txt)", type=["txt"])

parsed_lines = []
unique_characters = []

if uploaded_file is not None:
  raw_text = uploaded_file.read().decode("utf-8")
  parsed_lines = parse_script(raw_text)

  unique_characters = main_character(parsed_lines, min_lines=3)



  if not unique_characters:
    st.warning("No characters detected. This parser expects standard screenplay formatting (ALL CAPS name on its own line.")

else:
  with st.sidebar:
    st.info("Upload a .txt screenplay to begin. Standard format works best: ALL CAPS character names on their own line, after an INT./EXT. scene heading.")
  parsed_lines = []
  unique_characters = []

#dropdown for user to pick character
with st.sidebar:
  st.subheader("Your character")
  user_character = st.selectbox(
    "Select the character YOU are playing!:",
    options=unique_characters,
    disabled=(uploaded_file is None) #will not show until file is uploaded
)

load_disabled = uploaded_file is None or not user_character
if st.button("Load Script ", disabled=load_disabled):
  st.session_state.conversation.turns = [] #wipes previous scenes

  #ensures it showcases the character that is picked
  starting_idx = next(
    (i for i, line in enumerate(parsed_lines) if line.character == user_character), 0)
  st.session_state.current_line_idx = starting_idx 
  st.success("Script loaded! Ready to rehearse")

st.divider()



#PROGRESS BAR
idx = st.session_state.current_line_idx

if parsed_lines:
  st.subheader("Rehearsal")
  st.progress(idx / len(parsed_lines), text=f"Line {idx + 1} of {len(parsed_lines)}")

if st.session_state.get("last_error"):
  st.error(st.session_state.last_error)
  st.session_state.last_error = None

#check to make sure we didn't reach the end
if parsed_lines and idx < len(parsed_lines):
  upcoming = parsed_lines[idx]

  if upcoming.character == user_character:
    if st.button("Show my line"):
      st.caption(f"Your line : {upcoming.dialogue}")
  else:
    st.caption(f"Scene continues. {upcoming.character} speaks next.")
    next_line_pos = next_user_line_idx(parsed_lines, idx, user_character)

    #cacluates the gap distance
    if next_line_pos is None:

      #FIXED: before if never speak again, gap distance = INFINITE
      gap = next_line_pos - idx
      has_long_gap = True
      
     
      st.success("That's all of your character's lines. Nice work!")
    else:
       
      gap = next_line_pos - idx
      if gap > SKIP_GAP_COUNT:
        st.info(f"Your next line is {gap} lines away")
        if st.button("Skip to my next scene/line"):
          st.session_state.conversation.turns = []
          st.session_state.current_line_idx = next_line_pos
          st.rerun()


    #doesn't keep the user waiting for lines
    if st.button("Continue Scene"):
      convo = st.session_state.conversation
      next_idx = advance_through_other_characters(convo, parsed_lines, idx, user_character, MAX_AI_TURNS_PER_CLICK)
      
      st.session_state.current_line_idx = next_idx
      st.rerun()

##showcasing the rehearsal

with st.form(key="rehearse_form", clear_on_submit=True):
  next_line = st.text_input("Enter your next line:")
  submitted = st.form_submit_button(
    "Rehearse", disabled=(uploaded_file is None or not user_character)
  )   

#submit handler
if submitted:
  if not next_line.strip():
    st.warning("Type a line first.")
  elif idx >= len(parsed_lines):
    st.info("You've reached the end of the script!")
  else: 
    convo = st.session_state.conversation
    convo.add_actor_line(user_character, next_line)
    next_idx = advance_through_other_characters(convo, parsed_lines, idx + 1, user_character, MAX_AI_TURNS_PER_CLICK)

    st.session_state.current_line_idx = next_idx
    st.rerun() #runs twice so it stops this execution and start a fresh script from the top.




## will implement this for improv mode 
#character = st.text_input("Enter your scene partner's character: ",key='scene_partner')
#context = st.text_area("Enter the context of the scene(up to 3-5 sentences): ",key='context')
#line = st.text_input("Enter your line: ",key='line')



def render_turn(turn):
  speaker = turn.get('character', 'You' if turn["role"] == "user" else "Partner")
  avatar = "🎤" if turn["role"] == "user" else "🎭"
  with st.chat_message(turn["role"], avatar=avatar):
    st.markdown(f"**{speaker}**")
    st.write(turn["content"])


st.divider()
st.subheader("Transcript")

#collapses the old turns so user don't have to keep scrolling
MAX_VISIBLE_TURNS = 20
turns = rehearsal.conversation.turns if rehearsal is not None else []

if not turns:
  st.caption("Dialogue from this rehearsal will appear here.")


if len(turns) > MAX_VISIBLE_TURNS:
  hidden = turns[:-MAX_VISIBLE_TURNS]
  visible = turns[-MAX_VISIBLE_TURNS:]

  #saves the previous lines as well when it get removed 
  with st.expander(f"Show {len(hidden)} earlier line(s)"):
    for turn in hidden:
      render_turn(turn)
else:
  visible = turns

for turn in visible:
  render_turn(turn)









