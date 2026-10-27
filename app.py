import streamlit as st
from config import settings
from core import get_ai_response, AIClientError, build_scene_prompt, RehearsalSession, script_fingerprint, parse_script, main_character

#ui-elements
st.set_page_config(page_title="AI Theatre Coach", page_icon="🎭", layout="wide")
st.title("🎭 AI Theatre Coach")
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
  st.header("Rehearsal setup")
  uploaded_file = st.file_uploader("Screenplay (.txt)", type=["txt"])

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
  user_character = st.selectbox(
    "Your character",
    options=unique_characters,
    disabled=(uploaded_file is None) #will not show until file is uploaded
)

load_disabled = uploaded_file is None or not user_character
with st.sidebar:
  if st.button(
    "Start New Rehearsal",
    key="start_rehearsal",
    type="primary",
    use_container_width=True,
    disabled=load_disabled,
  ):
    st.session_state.rehearsal = RehearsalSession.start(
      raw_text=raw_text,
      script_name=uploaded_file.name,
      lines=parsed_lines,
      actor=user_character,
      max_history_turns=settings.MAX_HISTORY_TURNS,
    )
    st.success("New rehearsal ready.")

  sidebar_rehearsal = st.session_state.rehearsal
  if sidebar_rehearsal is not None:
    st.divider()
    st.caption("ACTIVE REHEARSAL")
    st.markdown(f"**{sidebar_rehearsal.script_name}**")
    st.write(f"Your role: **{sidebar_rehearsal.actor}**")

    draft_script_id = script_fingerprint(raw_text) if uploaded_file is not None else None
    if (
      draft_script_id != sidebar_rehearsal.script_id
      or user_character != sidebar_rehearsal.actor
    ):
      st.info("Setup changed. Start a new rehearsal to apply these choices.")

    if st.button(
      "Restart Rehearsal",
      key="restart_rehearsal",
      use_container_width=True,
      help="Return to your first cue and clear this rehearsal's transcript.",
    ):
      restart_rehearsal()
      st.rerun()



#PROGRESS BAR
rehearsal = st.session_state.rehearsal
active_lines = rehearsal.lines if rehearsal is not None else ()
active_actor = rehearsal.actor if rehearsal is not None else None
idx = rehearsal.current_line_idx if rehearsal is not None else 0

if rehearsal is not None:
  upcoming_character = (
    active_lines[idx].character if idx < len(active_lines) else "Complete"
  )
  st.header("Rehearsal workspace")
  script_col, actor_col, turn_col = st.columns(3)
  script_col.metric("Screenplay", rehearsal.script_name)
  actor_col.metric("Your role", active_actor)
  turn_col.metric("Current turn", upcoming_character)

  completed_position = min(idx, len(active_lines))
  visible_line = min(idx + 1, len(active_lines))
  st.progress(
    completed_position / len(active_lines),
    text=f"Line {visible_line} of {len(active_lines)}",
  )
else:
  st.info("Upload a screenplay, choose your character, and start a rehearsal.")

if rehearsal is not None and rehearsal.last_error:
  st.error(rehearsal.last_error)
  rehearsal.last_error = None

#check to make sure we didn't reach the end
if rehearsal is not None:
  with st.container(border=True):
    st.caption("CURRENT CUE")
    if idx < len(active_lines):
      upcoming = active_lines[idx]

      if upcoming.character == active_actor:
        st.subheader(f"Your turn · {active_actor}")
        st.caption("Deliver your next line when you're ready.")
        if st.button("Show My Line"):
          st.info(upcoming.dialogue)
      else:
        st.subheader(f"{upcoming.character}'s turn")
        st.caption("Continue when you're ready to hear the next partner line.")
        next_line_pos = next_user_line_idx(active_lines, idx, active_actor)

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
              rehearsal.conversation.turns = []
              rehearsal.current_line_idx = next_line_pos
              st.rerun()


        #doesn't keep the user waiting for lines
        if st.button("Continue Scene", type="primary"):
          next_idx = advance_through_other_characters(rehearsal, idx, MAX_AI_TURNS_PER_CLICK)

          rehearsal.current_line_idx = next_idx
          st.rerun()
    else:
      st.success("Rehearsal complete. Restart from the sidebar to run it again.")

##showcasing the rehearsal

st.subheader("Your line")
with st.form(key="rehearse_form", clear_on_submit=True):
  next_line = st.text_input("Enter your next line:")
  submitted = st.form_submit_button(
    "Rehearse", disabled=(rehearsal is None)
  )   

#submit handler
if submitted:
  if not next_line.strip():
    st.warning("Type a line first.")
  elif idx >= len(active_lines):
    st.info("You've reached the end of the script!")
  else: 
    convo = rehearsal.conversation
    convo.add_actor_line(active_actor, next_line)
    next_idx = advance_through_other_characters(rehearsal, idx + 1, MAX_AI_TURNS_PER_CLICK)

    rehearsal.current_line_idx = next_idx
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









