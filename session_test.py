import streamlit as st

if 'rehearse_count' not in st.session_state or 'conversation' not in st.session_state:
  st.session_state['rehearse_count'] = 0
  st.session_state['conversation'] = []

st.title("Testing")
user_input = st.text_input("Enter your character: ")


if st.button("Rehearse"):
  st.session_state.rehearse_count += 1
  st.session_state.conversation.append(user_input)
  st.write(st.session_state.rehearse_count)
  st.write(st.session_state.conversation)
