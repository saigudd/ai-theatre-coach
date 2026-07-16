import streamlit as st

st.title("AI Line Partner")

line = st.text_input("Enter your line: ")

if st.button("Reharse"):
  st.write(line)